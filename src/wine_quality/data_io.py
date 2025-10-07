"""Funciones de entrada/salida de datos para el dataset de vinos."""
from __future__ import annotations

from pathlib import Path
import pandas as pd


def _project_root() -> Path:
	# src/wine_quality/data_io.py -> parents[2] = raíz del proyecto
	return Path(__file__).resolve().parents[2]


def load_wine_data(root: str | Path | None = None) -> pd.DataFrame:
	"""Carga y concatena los datasets de vino tinto y blanco.

	Añade la columna 'wine_type'.

	Parameters
	----------
	root: Path opcional de la raíz del proyecto. Si no se pasa se infiere.

	Returns
	-------
	pd.DataFrame
		DataFrame combinado.
	"""

	base = Path(root) if root else _project_root()
	red_path = base / "data" / "raw" / "winequality-red.csv"
	white_path = base / "data" / "raw" / "winequality-white.csv"

	if not red_path.exists() or not white_path.exists():
		raise FileNotFoundError("No se encuentran los archivos raw de vino en data/raw/")

	df_red = pd.read_csv(red_path, sep=";")
	df_white = pd.read_csv(white_path, sep=";")

	df_red["wine_type"] = "red"
	df_white["wine_type"] = "white"

	df = pd.concat([df_red, df_white], ignore_index=True)
	return df
