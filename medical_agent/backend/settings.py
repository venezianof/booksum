import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    def load_dotenv(*_args, **_kwargs):
        return False


def _to_bool(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    value = value.strip().lower()
    if value in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "f", "no", "n", "off"}:
        return False
    return default


@dataclass(frozen=True)
class Settings:
    llm_provider: str = "local"

    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    openai_temperature: float = 0.2

    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-sonnet-20240229"

    huggingface_api_key: Optional[str] = None
    huggingface_model: str = "mistralai/Mistral-7B-Instruct-v0.1"

    pubmed_api_key: Optional[str] = None

    request_timeout_seconds: float = 8.0

    enable_cache: bool = True
    cache_ttl_seconds: int = 3600

    max_pubmed_results: int = 5

    @classmethod
    def from_env(cls) -> "Settings":
        env_path = Path(__file__).resolve().parents[1] / ".env"
        load_dotenv(env_path, override=False)

        llm_provider = os.getenv("LLM_PROVIDER", "local").strip().lower()

        openai_api_key = os.getenv("OPENAI_API_KEY")
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

        request_timeout_seconds = float(os.getenv("REQUEST_TIMEOUT", "8"))

        enable_cache = _to_bool(os.getenv("ENABLE_CACHE"), True)
        cache_ttl_seconds = int(os.getenv("CACHE_TTL", "3600"))

        max_pubmed_results = int(os.getenv("MAX_PUBMED_RESULTS", os.getenv("MAX_RESULTS", "5")))

        pubmed_api_key = os.getenv("PUBMED_API_KEY")

        openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", os.getenv("TEMPERATURE", "0.2")))

        settings = cls(
            llm_provider=llm_provider,
            openai_api_key=openai_api_key,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            openai_temperature=openai_temperature,
            anthropic_api_key=anthropic_api_key,
            anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
            huggingface_api_key=huggingface_api_key,
            huggingface_model=os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.1"),
            pubmed_api_key=pubmed_api_key,
            request_timeout_seconds=request_timeout_seconds,
            enable_cache=enable_cache,
            cache_ttl_seconds=cache_ttl_seconds,
            max_pubmed_results=max_pubmed_results,
        )

        if settings.llm_provider == "openai" and not settings.openai_api_key:
            return cls(**{**settings.__dict__, "llm_provider": "local"})
        if settings.llm_provider == "anthropic" and not settings.anthropic_api_key:
            return cls(**{**settings.__dict__, "llm_provider": "local"})
        if settings.llm_provider == "huggingface" and not settings.huggingface_api_key:
            return cls(**{**settings.__dict__, "llm_provider": "local"})

        return settings
