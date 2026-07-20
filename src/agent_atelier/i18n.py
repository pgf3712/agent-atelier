"""Minimal translation catalog loader with strict key parity."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CATALOG_DIR = Path(__file__).with_name("locales")
SUPPORTED_LOCALES = ("en", "es")
DEFAULT_LOCALE = "en"


def load_catalog(locale: str) -> dict[str, str]:
    normalized = locale.lower().split("-")[0]
    if normalized not in SUPPORTED_LOCALES:
        normalized = DEFAULT_LOCALE
    path = CATALOG_DIR / f"{normalized}.json"
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    if not all(isinstance(key, str) and isinstance(value, str) for key, value in data.items()):
        raise ValueError(f"Catalog {path.name} must contain string keys and values only.")
    return data  # type: ignore[return-value]


def validate_catalogs() -> None:
    catalogs = {locale: load_catalog(locale) for locale in SUPPORTED_LOCALES}
    expected = set(catalogs[DEFAULT_LOCALE])
    for locale, catalog in catalogs.items():
        missing = expected - set(catalog)
        extra = set(catalog) - expected
        if missing or extra:
            raise ValueError(
                f"Translation key mismatch for {locale}: "
                f"missing={sorted(missing)}, extra={sorted(extra)}"
            )


def translate(key: str, locale: str = DEFAULT_LOCALE, **values: object) -> str:
    catalog = load_catalog(locale)
    if key not in catalog:
        raise KeyError(f"Missing translation key: {key}")
    return catalog[key].format(**values)
