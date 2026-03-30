from __future__ import annotations

import os
import tempfile
from pathlib import Path


def configure_matplotlib_cache() -> None:
    cache_dir = Path(tempfile.gettempdir()) / "king_county_matplotlib"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))


def get_secret(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st

        if name in st.secrets:
            secret_value = st.secrets[name]
            return str(secret_value) if secret_value is not None else default
    except Exception:
        pass

    return default
