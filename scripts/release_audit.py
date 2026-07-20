"""Fail the public release when private or development-only material is present."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "README.md",
    "README.es.md",
    "COPYRIGHT.md",
    "SECURITY.md",
    "ASSET_CREDITS.md",
    "pyproject.toml",
    ".env.example",
    ".github/workflows/quality.yml",
}
PUBLICLY_FORBIDDEN = {
    "AUDIT_REPORT.md",
    "PROJECT_BIBLE.md",
    "references",
    ".env",
}
IGNORED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
TEXT_SUFFIXES = {
    ".bat", ".css", ".html", ".ini", ".js", ".json", ".md", ".ps1", ".py", ".toml", ".txt", ".yml", ".yaml"
}
SECRET_PATTERNS = {
    "OpenAI-style secret": re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    "GitHub token": re.compile(r"(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private key": re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    "development desktop path": re.compile(r"D:\\WINDOWS\\Escritorio", re.IGNORECASE),
}
PUBLIC_COPY_PATTERNS = {
    "interview-preparation material": re.compile(
        r"INTERVIEW_GUIDE|interview guide|recruiter tour|30[- ]second interview answer",
        re.IGNORECASE,
    ),
    "material de preparación de entrevistas": re.compile(
        r"gu[ií]a de entrevistas?|respuesta de entrevista|recorrido para reclutadores?",
        re.IGNORECASE,
    ),
}


def public_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in IGNORED_PARTS for part in path.parts)
    ]


def main() -> int:
    problems: list[str] = []

    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            problems.append(f"missing required file: {relative}")

    for relative in sorted(PUBLICLY_FORBIDDEN):
        if (ROOT / relative).exists():
            problems.append(f"development-only material is present: {relative}")

    for path in public_files():
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            problems.append(f"symbolic link requires manual review: {relative}")
            continue
        if path.name == Path(__file__).name:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {".gitignore", ".env.example"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    problems.append(f"{label} found in {relative}")
            for label, pattern in PUBLIC_COPY_PATTERNS.items():
                if pattern.search(text):
                    problems.append(f"{label} found in {relative}")
        else:
            sample = path.read_bytes().lower()
            for marker in (b"c:\\users\\", b"d:\\windows\\escritorio", b"openai_api_key="):
                if marker in sample:
                    problems.append(f"private marker found in binary file: {relative}")
                    break

    if problems:
        print("PUBLIC RELEASE AUDIT: FAILED")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"PUBLIC RELEASE AUDIT: PASS ({len(public_files())} files inspected)")
    print("No development-only files, local user paths or common secret formats detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
