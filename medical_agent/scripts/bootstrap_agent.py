#!/usr/bin/env python3

import argparse
import getpass
import secrets
import shutil
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Optional


_KEY_LINE_RE = re.compile(r"^(\s*)(#\s*)?([A-Z0-9_]+)=(.*)$")


@dataclass
class EnvFile:
    path: Path
    lines: list[str]

    @classmethod
    def load(cls, path: Path) -> "EnvFile":
        if not path.exists():
            return cls(path=path, lines=[])
        return cls(path=path, lines=path.read_text(encoding="utf-8").splitlines(True))

    def get(self, key: str) -> Optional[str]:
        for line in self.lines:
            m = _KEY_LINE_RE.match(line.rstrip("\n"))
            if not m:
                continue
            _, _, k, v = m.groups()
            if k == key:
                return v.strip()
        return None

    def set(self, key: str, value: str) -> None:
        replacement = f"{key}={value}\n"
        for i, line in enumerate(self.lines):
            m = _KEY_LINE_RE.match(line.rstrip("\n"))
            if not m:
                continue
            indent, _comment, k, _v = m.groups()
            if k == key:
                self.lines[i] = f"{indent}{replacement}"
                return
        if self.lines and not self.lines[-1].endswith("\n"):
            self.lines[-1] = self.lines[-1] + "\n"
        self.lines.append(replacement)

    def write(self) -> None:
        content = "".join(self.lines)
        if content and not content.endswith("\n"):
            content += "\n"
        self.path.write_text(content, encoding="utf-8")


def _is_placeholder(value: Optional[str]) -> bool:
    if value is None:
        return True
    v = value.strip().lower()
    if not v:
        return True
    return v in {
        "your-secret-key-here",
        "your-openai-api-key-here",
        "your-anthropic-api-key-here",
        "your-huggingface-api-key-here",
        "your-pubmed-api-key-here",
        "your-serper-api-key-here",
        "your-serpapi-api-key-here",
    }


def _prompt_choice(prompt: str, choices: list[str], default: str) -> str:
    choice_str = "/".join(choices)
    while True:
        raw = input(f"{prompt} [{choice_str}] (default: {default}): ").strip().lower()
        if not raw:
            return default
        if raw in choices:
            return raw
        print(f"Please choose one of: {', '.join(choices)}")


def _prompt_bool(prompt: str, default: bool) -> bool:
    default_str = "y" if default else "n"
    while True:
        raw = input(f"{prompt} [y/n] (default: {default_str}): ").strip().lower()
        if not raw:
            return default
        if raw in {"y", "yes", "true", "1"}:
            return True
        if raw in {"n", "no", "false", "0"}:
            return False
        print("Please enter 'y' or 'n'.")


def _prompt_text(prompt: str, default: Optional[str] = None) -> str:
    suffix = f" (default: {default})" if default else ""
    raw = input(f"{prompt}{suffix}: ").strip()
    return raw if raw else (default or "")


def _prompt_secret(prompt: str, default: Optional[str] = None, required: bool = False) -> str:
    while True:
        raw = getpass.getpass(
            f"{prompt}{' (press Enter to keep existing)' if default else ''}: "
        ).strip()
        if raw:
            return raw
        if default and not _is_placeholder(default):
            return default
        if not required:
            return ""
        print("This value is required for the selected configuration.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Bootstrap the Medical Agent by creating/updating a .env file. "
            "Safe to re-run."
        )
    )
    parser.add_argument(
        "--defaults",
        action="store_true",
        help=(
            "Use safe defaults (local LLM provider, web search disabled) without prompting. "
            "Produces a usable .env for running the demo."
        ),
    )
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parents[1]
    env_example = project_dir / ".env.example"
    env_path = project_dir / ".env"

    if not env_example.exists():
        print(f"ERROR: Missing template file: {env_example}")
        return 1

    if not env_path.exists():
        shutil.copy(env_example, env_path)
        print("Created .env from .env.example")
    else:
        print("Found existing .env — updating it in place (no duplicate keys will be created).")

    env_file = EnvFile.load(env_path)

    # Always ensure SECRET_KEY is set to something non-placeholder.
    secret_key = env_file.get("SECRET_KEY")
    if _is_placeholder(secret_key):
        env_file.set("SECRET_KEY", secrets.token_hex(32))

    if args.defaults:
        provider = "local"
    else:
        provider = _prompt_choice(
            "Select LLM provider",
            choices=["local", "openai", "anthropic", "huggingface"],
            default=(env_file.get("LLM_PROVIDER") or "local").lower(),
        )

    env_file.set("LLM_PROVIDER", provider)

    if provider == "openai":
        existing = env_file.get("OPENAI_API_KEY")
        key = _prompt_secret("OpenAI API key (OPENAI_API_KEY)", default=existing, required=True)
        env_file.set("OPENAI_API_KEY", key)
        model = _prompt_text("OpenAI model (OPENAI_MODEL)", default=env_file.get("OPENAI_MODEL") or "gpt-4o-mini")
        env_file.set("OPENAI_MODEL", model)

    elif provider == "anthropic":
        existing = env_file.get("ANTHROPIC_API_KEY")
        key = _prompt_secret("Anthropic API key (ANTHROPIC_API_KEY)", default=existing, required=True)
        env_file.set("ANTHROPIC_API_KEY", key)
        model = _prompt_text(
            "Anthropic model (ANTHROPIC_MODEL)",
            default=env_file.get("ANTHROPIC_MODEL") or "claude-3-5-sonnet-20241022",
        )
        env_file.set("ANTHROPIC_MODEL", model)

    elif provider == "huggingface":
        existing = env_file.get("HUGGINGFACE_API_KEY")
        key = _prompt_secret("HuggingFace API key (HUGGINGFACE_API_KEY)", default=existing, required=True)
        env_file.set("HUGGINGFACE_API_KEY", key)
        model = _prompt_text(
            "HuggingFace model (HUGGINGFACE_MODEL)",
            default=env_file.get("HUGGINGFACE_MODEL") or "mistralai/Mistral-7B-Instruct-v0.1",
        )
        env_file.set("HUGGINGFACE_MODEL", model)

    if args.defaults:
        enable_web_search = False
    else:
        enable_web_search = _prompt_bool(
            "Enable web search tool? (requires SERPER_API_KEY or SERPAPI_API_KEY)",
            default=(env_file.get("ENABLE_WEB_SEARCH") or "false").lower() in {"1", "true", "yes", "y"},
        )

    env_file.set("ENABLE_WEB_SEARCH", "true" if enable_web_search else "false")

    if enable_web_search and not args.defaults:
        provider_choice = _prompt_choice(
            "Choose web search API",
            choices=["serper", "serpapi"],
            default="serper" if env_file.get("SERPER_API_KEY") else "serpapi",
        )
        if provider_choice == "serper":
            existing = env_file.get("SERPER_API_KEY")
            key = _prompt_secret("Serper API key (SERPER_API_KEY)", default=existing, required=True)
            env_file.set("SERPER_API_KEY", key)
        else:
            existing = env_file.get("SERPAPI_API_KEY")
            key = _prompt_secret("SerpAPI key (SERPAPI_API_KEY)", default=existing, required=True)
            env_file.set("SERPAPI_API_KEY", key)

    env_file.write()

    print("\nDone. Next steps:")
    print("  1) (Optional) Review and tweak medical_agent/.env")
    print("  2) Install deps:    cd medical_agent && pip install -r requirements.txt")
    print("  3) Run the server:  cd medical_agent/backend && python app.py")
    print("\nIf you change providers later, re-run this script; it will update your .env safely.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
