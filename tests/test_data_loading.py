"""Tests for data loading.

Se añade manipulación de sys.path para poder importar el paquete sin instalación editable.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wine_quality import load_wine_data  # noqa: E402


def test_load_wine_data_basic():
    df = load_wine_data()
    assert not df.empty
    assert "wine_type" in df.columns
    assert df["wine_type"].isin(["red", "white"]).all()
    assert df["quality"].between(0, 10).all()
