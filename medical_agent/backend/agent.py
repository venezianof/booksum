import logging
from typing import Any, Dict, List, Optional

from services.llm_client import LLMClient
from services.pubmed_client import PubMedArticle, PubMedClient
from settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MEDICAL_DISCLAIMER = (
    "⚠️ DISCLAIMER: This information is for educational purposes only and is NOT medical advice. "
    "It does not replace professional diagnosis, treatment, or individualized clinical judgment. "
    "Always consult a qualified healthcare provider for medical decisions."
)


class MedicalResearchAgent:
    """Answers medical questions using PubMed lookups + an optional LLM summarizer."""

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings.from_env()

        self.pubmed = PubMedClient(
            api_key=self.settings.pubmed_api_key,
            timeout_seconds=self.settings.request_timeout_seconds,
            enable_cache=self.settings.enable_cache,
            cache_ttl_seconds=self.settings.cache_ttl_seconds,
        )

        self.llm = LLMClient(
            provider=self.settings.llm_provider,
            openai_api_key=self.settings.openai_api_key,
            openai_model=self.settings.openai_model,
            openai_temperature=self.settings.openai_temperature,
            anthropic_api_key=self.settings.anthropic_api_key,
            anthropic_model=self.settings.anthropic_model,
            huggingface_api_key=self.settings.huggingface_api_key,
            huggingface_model=self.settings.huggingface_model,
            request_timeout_seconds=self.settings.request_timeout_seconds,
        )

        logger.info(
            "MedicalResearchAgent initialized (llm_provider=%s, cache=%s)",
            self.settings.llm_provider,
            self.settings.enable_cache,
        )

    def _validate_question(self, question: str) -> Dict[str, Any]:
        q = (question or "").strip()
        if not q:
            return {"ok": False, "question": "", "error": "Empty question"}

        truncated = False
        if len(q) > 5000:
            q = q[:5000]
            truncated = True

        return {"ok": True, "question": q, "truncated": truncated}

    def _articles_to_sources(self, articles: List[PubMedArticle]) -> List[Dict[str, Any]]:
        sources: List[Dict[str, Any]] = []
        for a in articles:
            sources.append(
                {
                    "title": a.title,
                    "snippet": a.snippet,
                    "journal": a.journal,
                    "publication_date": a.publication_date,
                    "url": a.url,
                    "pmid": a.pmid,
                }
            )
        return sources

    def ask(self, question: str) -> dict:
        """Process a medical research question and return structured output.

        Returns a dict with:
        - answer_text: str
        - bullets: List[str] (>=3)
        - source_links: List[Dict[str, Any]]
        - disclaimer: str
        - analysis: optional metadata
        """

        validation = self._validate_question(question)
        if not validation.get("ok"):
            return {
                "answer_text": "Please provide a non-empty medical research question.",
                "bullets": [
                    "Try asking a specific question (e.g., condition + treatment + timeframe).",
                    "Example: 'What do recent clinical trials say about GLP-1 medications for type 2 diabetes?'",
                    "This tool provides educational information only; consult a clinician for medical advice.",
                ],
                "source_links": [],
                "disclaimer": MEDICAL_DISCLAIMER,
                "analysis": {"error": validation.get("error")},
            }

        q = validation["question"]
        logger.info("Received question: %s", q)

        articles: List[PubMedArticle] = []
        pubmed_meta: Dict[str, Any] = {}

        try:
            articles, pubmed_meta = self.pubmed.search(q, retmax=self.settings.max_pubmed_results)
        except Exception as e:
            logger.warning("PubMed lookup failed: %s", e)
            pubmed_meta = {"error": "PubMed lookup failed"}
            articles = []

        llm_outputs = self.llm.summarize(q, articles)

        sources = self._articles_to_sources(articles)

        response: Dict[str, Any] = {
            "answer_text": llm_outputs.answer_text,
            "bullets": llm_outputs.bullets,
            "source_links": sources if sources else [{"title": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/"}],
            "disclaimer": MEDICAL_DISCLAIMER,
            "analysis": {
                "question_truncated": bool(validation.get("truncated")),
                "pubmed": pubmed_meta,
                "llm": {"provider": self.settings.llm_provider, "used_llm": llm_outputs.used_llm},
            },
        }

        if llm_outputs.recommendations:
            response["recommendations"] = llm_outputs.recommendations

        return response
