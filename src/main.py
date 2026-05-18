"""Single entry point for the Circuit Tutor Streamlit app."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.web import cli as stcli

from utils.helpers import get_asset_path


SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
PAGES_DIR = SRC_DIR / "ui" / "pages"
HOME_PAGE = SRC_DIR / "ui" / "home.py"
ICON_PATH = get_asset_path("icon.ico")


def ensure_src_on_path() -> None:
    """Allow absolute imports like `from utils import helpers`."""
    src_dir = str(SRC_DIR)
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)


def page_title_from_path(page_path: Path) -> str:
    """Convert filenames such as `1_Ohms_Law.py` into readable labels."""
    name = page_path.stem
    if "_" in name:
        _, name = name.split("_", 1)
    return name.replace("_", " ")


def discover_pages() -> list[tuple[str, Path]]:
    """Return Streamlit page scripts in numeric filename order."""
    return [
        (page_title_from_path(page_path), page_path)
        for page_path in sorted(PAGES_DIR.glob("*.py"))
    ]


def run_page(page_path: Path) -> None:
    """Execute a page script inside the active Streamlit session."""
    runpy.run_path(str(page_path), run_name="__main__")


def render_app() -> None:
    """Render the app shell and dispatch the selected page."""
    ensure_src_on_path()

    st.set_page_config(
        page_title="Circuit Tutor",
        page_icon=str(ICON_PATH) if ICON_PATH.exists() else None,
        layout="centered",
    )

    available_pages = [("Home", HOME_PAGE), *discover_pages()]
    page_lookup = {title: path for title, path in available_pages}

    with st.sidebar:
        st.title("Circuit Tutor")
        selected_page = st.radio(
            "Choose a page",
            options=[title for title, _ in available_pages],
        )

    run_page(page_lookup[selected_page])


def launch_streamlit() -> None:
    """Re-run this file through Streamlit when started with plain Python."""
    ensure_src_on_path()
    sys.argv = ["streamlit", "run", str(Path(__file__).resolve())]
    raise SystemExit(stcli.main())


if __name__ == "__main__":
    if get_script_run_ctx() is None:
        launch_streamlit()
    else:
        render_app()
