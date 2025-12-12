import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from services.pubmed_client import PubMedArticle

logger = logging.getLogger(__name__)


def _ensure_min_bullets(bullets: List[str], minimum: int = 3) -> List[str]:
    cleaned = [b.strip().lstrip("-• ").strip() for b in bullets if isinstance(b, str) and b.strip()]
    while len(cleaned) < minimum:
        cleaned.append(
            "This is educational information, not medical advice; discuss individual care with a licensed clinician."
        )
    return cleaned[: max(minimum, len(cleaned))]


def _try_parse_json(text: str) -> Optional[Dict[str, Any]]:
    text = (text or "").strip()
    if not text:
        return None

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except Exception:
        return None


@dataclass(frozen=True)
class LLMOutputs:
    answer_text: str
    bullets: List[str]
    recommendations: List[str]
    used_llm: bool


class LLMClient:
    ANSWER_TEMPLATE = (
        "You are a medical research assistant. Provide an educational summary to the user's question, "
        "grounded in the provided PubMed citations. Avoid giving personal medical advice."
    )

    BULLETS_TEMPLATE = (
        "Provide at least 3 concise bullet insights that reflect themes from the citations (mechanism, evidence, safety, etc.)."
    )

    RECOMMENDATIONS_TEMPLATE = (
        "Provide a short list of 2-4 recommendations for what the user should read/verify next (e.g., guidelines, RCTs, reviews)."
    )

    def __init__(
        self,
        provider: str = "local",
        openai_api_key: Optional[str] = None,
        openai_model: str = "gpt-3.5-turbo",
        openai_temperature: float = 0.2,
        anthropic_api_key: Optional[str] = None,
        anthropic_model: str = "claude-3-sonnet-20240229",
        huggingface_api_key: Optional[str] = None,
        huggingface_model: str = "mistralai/Mistral-7B-Instruct-v0.1",
        request_timeout_seconds: float = 8.0,
    ):
        self._provider = (provider or "local").lower()
        self._model = None
        self._used_llm = False

        if self._provider == "openai" and openai_api_key:
            self._model = self._init_openai(openai_api_key, openai_model, openai_temperature, request_timeout_seconds)
        elif self._provider == "anthropic" and anthropic_api_key:
            self._model = self._init_anthropic(anthropic_api_key, anthropic_model, request_timeout_seconds)
        elif self._provider == "huggingface" and huggingface_api_key:
            self._model = self._init_huggingface(huggingface_api_key, huggingface_model)

        if self._model is None:
            self._provider = "local"

    def _init_openai(self, api_key: str, model: str, temperature: float, timeout_seconds: float):
        try:
            try:
                from langchain_community.chat_models import ChatOpenAI
            except Exception:  # pragma: no cover
                from langchain.chat_models import ChatOpenAI  # type: ignore

            for kwargs in (
                {
                    "openai_api_key": api_key,
                    "model_name": model,
                    "temperature": temperature,
                    "request_timeout": timeout_seconds,
                },
                {
                    "api_key": api_key,
                    "model": model,
                    "temperature": temperature,
                    "timeout": timeout_seconds,
                },
            ):
                try:
                    return ChatOpenAI(**kwargs)
                except TypeError:
                    continue

            return None
        except Exception as e:
            logger.info("OpenAI chat model unavailable, falling back to local: %s", e)
            return None

    def _init_anthropic(self, api_key: str, model: str, timeout_seconds: float):
        try:
            try:
                from langchain_community.chat_models import ChatAnthropic
            except Exception:  # pragma: no cover
                from langchain.chat_models import ChatAnthropic  # type: ignore

            for kwargs in (
                {"anthropic_api_key": api_key, "model": model, "timeout": timeout_seconds},
                {"anthropic_api_key": api_key, "model_name": model, "timeout": timeout_seconds},
            ):
                try:
                    return ChatAnthropic(**kwargs)
                except TypeError:
                    continue

            return None
        except Exception as e:
            logger.info("Anthropic chat model unavailable, falling back to local: %s", e)
            return None

    def _init_huggingface(self, api_key: str, model: str):
        try:
            from langchain_community.llms import HuggingFaceHub

            return HuggingFaceHub(
                huggingfacehub_api_token=api_key,
                repo_id=model,
            )
        except Exception as e:
            logger.info("HuggingFace model unavailable, falling back to local: %s", e)
            return None

    def _format_sources(self, articles: List[PubMedArticle]) -> str:
        if not articles:
            return "(no PubMed sources available)"

        lines = []
        for idx, a in enumerate(articles, start=1):
            date = a.publication_date or "n.d."
            journal = a.journal or ""
            snippet = a.snippet or ""
            lines.append(
                f"[{idx}] {a.title} ({journal}; {date})\nURL: {a.url}\nSnippet: {snippet}"
            )
        return "\n\n".join(lines)

    def _heuristic_summarize(self, question: str, articles: List[PubMedArticle]) -> LLMOutputs:
        answer_parts = []
        if articles:
            answer_parts.append(
                f"I found {len(articles)} recent PubMed results that may be relevant. Below is a high-level summary of themes from the titles/abstract snippets."  # noqa: E501
            )
        else:
            answer_parts.append(
                "I couldn't retrieve PubMed results right now. Below is a general, educational overview and suggestions for how to verify the latest evidence."  # noqa: E501
            )

        titles = " ".join(a.title for a in articles)
        tokens = [t.lower() for t in re.findall(r"[A-Za-z][A-Za-z\-]{2,}", titles)]
        stop = {
            "with",
            "from",
            "into",
            "over",
            "under",
            "among",
            "between",
            "trial",
            "trials",
            "randomized",
            "randomised",
            "double",
            "blind",
            "study",
            "studies",
            "effect",
            "effects",
            "analysis",
            "meta",
            "systematic",
            "review",
            "patients",
            "patient",
            "treatment",
            "therapies",
            "therapy",
            "clinical",
            "results",
            "outcomes",
        }
        freq: Dict[str, int] = {}
        for t in tokens:
            if t in stop or len(t) < 4:
                continue
            freq[t] = freq.get(t, 0) + 1
        top_terms = [w for w, _ in sorted(freq.items(), key=lambda kv: kv[1], reverse=True)[:6]]

        if top_terms:
            answer_parts.append("Common topics in the retrieved citations: " + ", ".join(top_terms) + ".")

        answer_text = "\n\n".join(answer_parts).strip()

        bullets: List[str] = []
        if articles:
            bullets.append("Recent papers may cover multiple approaches (medications, devices, lifestyle, and care pathways).")
            bullets.append("Look for high-quality evidence first (guidelines, systematic reviews, large RCTs) before drawing conclusions.")
            bullets.append("Compare benefits vs. harms and consider patient-specific factors (age, comorbidities, pregnancy, kidney function).")
        else:
            bullets.append("PubMed was unreachable; if you need the very latest evidence, try again later or search PubMed directly.")
            bullets.append("Consider starting with major guideline sources (ADA, AHA, WHO, NICE) for current best practices.")
            bullets.append("If the question is urgent or personal, seek professional medical advice.")

        recommendations = [
            "Search PubMed for recent systematic reviews and randomized trials.",
            "Check the latest clinical guidelines from relevant professional societies.",
            "If a specific therapy is mentioned, review its safety profile, contraindications, and major trials.",
        ]

        return LLMOutputs(
            answer_text=answer_text,
            bullets=_ensure_min_bullets(bullets),
            recommendations=recommendations,
            used_llm=False,
        )

    def summarize(self, question: str, articles: List[PubMedArticle]) -> LLMOutputs:
        question = (question or "").strip()

        if self._model is None:
            return self._heuristic_summarize(question, articles)

        try:
            from langchain_core.messages import HumanMessage, SystemMessage

            sources_text = self._format_sources(articles)
            system = (
                "You are a careful medical research assistant. Provide educational information only. "
                "Do not provide diagnosis or personalized treatment plans."  # noqa: E501
            )
            user = (
                f"{self.ANSWER_TEMPLATE}\n\n{self.BULLETS_TEMPLATE}\n\n{self.RECOMMENDATIONS_TEMPLATE}\n\n"
                f"Question: {question}\n\nPubMed citations:\n{sources_text}\n\n"
                "Return a JSON object with keys: answer_text (string), bullets (list of strings), recommendations (list of strings)."
            )

            resp = self._model.invoke([SystemMessage(content=system), HumanMessage(content=user)])
            text = getattr(resp, "content", None) or str(resp)

            payload = _try_parse_json(text)
            if not payload:
                raise ValueError("LLM did not return valid JSON")

            answer_text = str(payload.get("answer_text") or "").strip()
            bullets = payload.get("bullets") or []
            recommendations = payload.get("recommendations") or []

            if not answer_text:
                raise ValueError("LLM output missing answer_text")

            self._used_llm = True
            return LLMOutputs(
                answer_text=answer_text,
                bullets=_ensure_min_bullets(list(bullets)),
                recommendations=[str(x).strip() for x in recommendations if str(x).strip()],
                used_llm=True,
            )
        except Exception as e:
            logger.info("LLM summarization failed; falling back to heuristic: %s", e)
            return self._heuristic_summarize(question, articles)
