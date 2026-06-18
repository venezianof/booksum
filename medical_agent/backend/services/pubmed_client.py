import logging
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests

from services.cache import TTLCache

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PubMedArticle:
    pmid: str
    title: str
    snippet: str
    journal: Optional[str]
    publication_date: Optional[str]
    url: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PubMedClient:
    """Thin wrapper around NCBI E-utilities for PubMed."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout_seconds: float = 8.0,
        enable_cache: bool = True,
        cache_ttl_seconds: int = 3600,
        tool: str = "medical_agent",
    ):
        self._base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds
        self._tool = tool

        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": "medical_agent/1.0 (+https://pubmed.ncbi.nlm.nih.gov/)",
            }
        )

        self._min_interval_seconds = 0.12 if api_key else 0.35
        self._last_request_at: Optional[float] = None

        self._enable_cache = enable_cache
        self._query_cache = TTLCache[Tuple[str, int], List[PubMedArticle]](ttl_seconds=cache_ttl_seconds)

    def _rate_limit(self) -> None:
        if self._last_request_at is None:
            return
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self._min_interval_seconds:
            time.sleep(self._min_interval_seconds - elapsed)

    def _get(self, endpoint: str, params: Dict[str, Any]) -> Optional[requests.Response]:
        url = f"{self._base_url}/{endpoint}"

        params = {k: v for k, v in params.items() if v is not None}
        if self._api_key:
            params["api_key"] = self._api_key
        params["tool"] = self._tool

        try:
            self._rate_limit()
            resp = self._session.get(url, params=params, timeout=self._timeout_seconds)
            self._last_request_at = time.monotonic()
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            logger.warning("PubMed request failed: %s", e)
            return None

    def _esearch(self, term: str, retmax: int) -> Tuple[List[str], Dict[str, Any]]:
        resp = self._get(
            "esearch.fcgi",
            {
                "db": "pubmed",
                "term": term,
                "retmode": "json",
                "retmax": retmax,
                "sort": "pub+date",
            },
        )
        if resp is None:
            return [], {"error": "PubMed esearch request failed"}

        try:
            data = resp.json()
            ids = data.get("esearchresult", {}).get("idlist", [])
            return [str(x) for x in ids], {"count": data.get("esearchresult", {}).get("count")}
        except Exception as e:
            logger.warning("PubMed esearch parse failed: %s", e)
            return [], {"error": "PubMed esearch parse failed"}

    def _esummary(self, pmids: List[str]) -> Tuple[List[PubMedArticle], Dict[str, Any]]:
        if not pmids:
            return [], {"pmids": []}

        resp = self._get(
            "esummary.fcgi",
            {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "json",
            },
        )
        if resp is None:
            return [], {"error": "PubMed esummary request failed"}

        try:
            data = resp.json()
            result = data.get("result", {})
            uids = result.get("uids", [])
            articles: List[PubMedArticle] = []
            for uid in uids:
                rec = result.get(str(uid), {})
                pmid = str(uid)
                title = (rec.get("title") or "").strip().rstrip(".")
                journal = rec.get("fulljournalname")
                pubdate = rec.get("pubdate")
                url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                snippet = title
                articles.append(
                    PubMedArticle(
                        pmid=pmid,
                        title=title or f"PubMed article {pmid}",
                        snippet=snippet,
                        journal=journal,
                        publication_date=pubdate,
                        url=url,
                    )
                )
            return articles, {"pmids": pmids}
        except Exception as e:
            logger.warning("PubMed esummary parse failed: %s", e)
            return [], {"error": "PubMed esummary parse failed"}

    def _efetch_abstracts(self, pmids: List[str]) -> Dict[str, str]:
        if not pmids:
            return {}

        resp = self._get(
            "efetch.fcgi",
            {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "xml",
            },
        )
        if resp is None:
            return {}

        try:
            root = ET.fromstring(resp.text)
        except Exception as e:
            logger.warning("PubMed efetch XML parse failed: %s", e)
            return {}

        abstracts: Dict[str, str] = {}
        for article in root.findall(".//PubmedArticle"):
            pmid_el = article.find(".//MedlineCitation/PMID")
            if pmid_el is None or not pmid_el.text:
                continue
            pmid = pmid_el.text.strip()
            abstract_parts = [
                (t.text or "").strip()
                for t in article.findall(".//Abstract/AbstractText")
                if (t.text or "").strip()
            ]
            if abstract_parts:
                abstracts[pmid] = " ".join(abstract_parts)
        return abstracts

    def search(self, query: str, retmax: int = 5) -> Tuple[List[PubMedArticle], Dict[str, Any]]:
        query = (query or "").strip()
        if not query:
            return [], {"error": "Empty query"}

        if self._enable_cache:
            cached = self._query_cache.get((query, retmax))
            if cached is not None:
                return cached, {"used_cache": True, "query": query, "retmax": retmax}

        pmids, meta_search = self._esearch(query, retmax=retmax)
        if not pmids:
            meta = {"query": query, "retmax": retmax, **meta_search}
            return [], meta

        articles, meta_summary = self._esummary(pmids)
        abstracts = self._efetch_abstracts(pmids[: min(3, len(pmids))])

        merged: List[PubMedArticle] = []
        for a in articles:
            abstract = abstracts.get(a.pmid)
            snippet = abstract.strip() if abstract else a.snippet
            if len(snippet) > 280:
                snippet = snippet[:277].rstrip() + "..."
            merged.append(
                PubMedArticle(
                    pmid=a.pmid,
                    title=a.title,
                    snippet=snippet,
                    journal=a.journal,
                    publication_date=a.publication_date,
                    url=a.url,
                )
            )

        meta = {"query": query, "retmax": retmax, **meta_search, **meta_summary, "used_cache": False}

        if self._enable_cache:
            self._query_cache.set((query, retmax), merged)

        return merged, meta
