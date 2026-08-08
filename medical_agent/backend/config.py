import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional, cast

from dotenv import load_dotenv


LLMProvider = Literal["openai", "anthropic", "huggingface", "local"]

_DOTENV_LOADED = False


def load_env_once(env_path: Optional[Path] = None, override: bool = False) -> Optional[Path]:
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return env_path

    base_dir = Path(__file__).resolve().parent.parent
    resolved = env_path or (base_dir / ".env")

    if resolved.exists():
        load_dotenv(dotenv_path=resolved, override=override)
        _DOTENV_LOADED = True
        return resolved

    _DOTENV_LOADED = True
    return None


def _is_truthy(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    v = value.strip().lower()
    if v in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "f", "no", "n", "off"}:
        return False
    return default


def _as_int(value: Optional[str], default: int) -> int:
    if value is None or not value.strip():
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _as_float(value: Optional[str], default: float) -> float:
    if value is None or not value.strip():
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _as_list(value: Optional[str], default: List[str]) -> List[str]:
    if value is None:
        return default
    items = [v.strip() for v in value.split(",")]
    return [v for v in items if v]


def _is_placeholder(value: Optional[str]) -> bool:
    if value is None:
        return True
    v = value.strip().lower()
    if not v:
        return True
    return v in {
        "your-openai-api-key-here",
        "your-anthropic-api-key-here",
        "your-huggingface-api-key-here",
    }


@dataclass(frozen=True)
class ServerConfig:
    flask_env: str
    flask_debug: bool
    port: int
    secret_key: str
    cors_origins: List[str]


@dataclass(frozen=True)
class LLMConfig:
    provider: LLMProvider
    model: Optional[str]
    temperature: float

    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None


@dataclass(frozen=True)
class AgentConfig:
    max_iterations: int
    max_tokens: int
    temperature: float
    enable_memory: bool
    memory_size: int


@dataclass(frozen=True)
class FeatureFlags:
    enable_experimental: bool
    enable_web_search: bool
    enable_pdf_parser: bool
    enable_citations: bool
    enable_cache: bool


@dataclass(frozen=True)
class Settings:
    server: ServerConfig
    llm: LLMConfig
    agent: AgentConfig
    features: FeatureFlags

    rate_limit: int
    request_timeout: int

    serper_api_key: Optional[str] = None
    serpapi_api_key: Optional[str] = None


def get_settings(env_path: Optional[Path] = None) -> Settings:
    load_env_once(env_path=env_path)

    provider = (os.getenv("LLM_PROVIDER") or "local").strip().lower()
    if provider not in {"openai", "anthropic", "huggingface", "local"}:
        raise ValueError(
            "Invalid LLM_PROVIDER. Expected one of: openai, anthropic, huggingface, local. "
            f"Got: {provider!r}."
        )
    llm_provider = cast(LLMProvider, provider)

    server = ServerConfig(
        flask_env=os.getenv("FLASK_ENV") or "development",
        flask_debug=_is_truthy(os.getenv("FLASK_DEBUG"), default=False),
        port=_as_int(os.getenv("PORT"), default=5000),
        secret_key=os.getenv("SECRET_KEY") or "dev-secret-key",
        cors_origins=_as_list(
            os.getenv("CORS_ORIGINS"),
            default=["http://localhost:3000", "http://localhost:5000"],
        ),
    )

    enable_web_search = _is_truthy(os.getenv("ENABLE_WEB_SEARCH"), default=False)
    features = FeatureFlags(
        enable_experimental=_is_truthy(os.getenv("ENABLE_EXPERIMENTAL"), default=False),
        enable_web_search=enable_web_search,
        enable_pdf_parser=_is_truthy(os.getenv("ENABLE_PDF_PARSER"), default=True),
        enable_citations=_is_truthy(os.getenv("ENABLE_CITATIONS"), default=True),
        enable_cache=_is_truthy(os.getenv("ENABLE_CACHE"), default=True),
    )

    agent = AgentConfig(
        max_iterations=_as_int(os.getenv("MAX_ITERATIONS"), default=10),
        max_tokens=_as_int(os.getenv("MAX_TOKENS"), default=2000),
        temperature=_as_float(os.getenv("TEMPERATURE"), default=0.7),
        enable_memory=_is_truthy(os.getenv("ENABLE_MEMORY"), default=True),
        memory_size=_as_int(os.getenv("MEMORY_SIZE"), default=10),
    )

    llm_temperature = _as_float(os.getenv("OPENAI_TEMPERATURE"), default=agent.temperature)
    model: Optional[str]

    if llm_provider == "openai":
        model = os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
    elif llm_provider == "anthropic":
        model = os.getenv("ANTHROPIC_MODEL")
    elif llm_provider == "huggingface":
        model = os.getenv("HUGGINGFACE_MODEL")
    else:
        model = None

    llm = LLMConfig(
        provider=llm_provider,
        model=model,
        temperature=llm_temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
    )

    serper_api_key = os.getenv("SERPER_API_KEY")
    serpapi_api_key = os.getenv("SERPAPI_API_KEY")

    if llm_provider == "openai" and _is_placeholder(llm.openai_api_key):
        raise ValueError(
            "LLM_PROVIDER=openai requires a valid OPENAI_API_KEY. "
            "Run 'python medical_agent/scripts/bootstrap_agent.py' to create/update your .env."
        )
    if llm_provider == "anthropic" and _is_placeholder(llm.anthropic_api_key):
        raise ValueError(
            "LLM_PROVIDER=anthropic requires a valid ANTHROPIC_API_KEY. "
            "Run 'python medical_agent/scripts/bootstrap_agent.py' to create/update your .env."
        )
    if llm_provider == "huggingface" and _is_placeholder(llm.huggingface_api_key):
        raise ValueError(
            "LLM_PROVIDER=huggingface requires a valid HUGGINGFACE_API_KEY. "
            "Run 'python medical_agent/scripts/bootstrap_agent.py' to create/update your .env."
        )

    if enable_web_search and not (serper_api_key and serper_api_key.strip()) and not (
        serpapi_api_key and serpapi_api_key.strip()
    ):
        raise ValueError(
            "ENABLE_WEB_SEARCH=true requires SERPER_API_KEY or SERPAPI_API_KEY. "
            "Either set one in your .env or disable web search."
        )

    return Settings(
        server=server,
        llm=llm,
        agent=agent,
        features=features,
        rate_limit=_as_int(os.getenv("RATE_LIMIT"), default=100),
        request_timeout=_as_int(os.getenv("REQUEST_TIMEOUT"), default=30),
        serper_api_key=serper_api_key,
        serpapi_api_key=serpapi_api_key,
    )
