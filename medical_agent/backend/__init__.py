from .config import get_settings, load_env_once

# Load medical_agent/.env once at import-time so other modules can rely on os.environ.
load_env_once()

__all__ = ["get_settings"]
