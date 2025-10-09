"""Utilidades de logging de métricas de entrenamiento.

Registra métricas en un CSV incremental (`outputs/metrics.csv`) para facilitar
el seguimiento de experimentos ligeros sin depender todavía de un tracker externo.

Diseño:
 - Append-only: no se reescriben filas previas.
 - Columnas dinámicas: se agregan nuevas si aparecen métricas adicionales.
 - Atributos extra opcionales (``extra``) para tags, artefactos, etc.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Mapping, Any
import csv


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _metrics_path(path: str | Path | None = None) -> Path:
    if path is None:
        return _project_root() / "outputs" / "metrics.csv"
    return Path(path)


def _ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def _flatten(d: Mapping[str, Any], prefix: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, Mapping):
            out.update(_flatten(v, key))
        else:
            out[key] = v
    return out


def log_metrics(model_name: str, metrics: Mapping[str, Any], *, extra: Mapping[str, Any] | None = None, path: str | Path | None = None) -> Path:
    """Loggea métricas a un CSV.

    Params
    ------
    model_name: nombre lógico del modelo/experimento.
    metrics: dict de métricas numéricas o anidadas (se aplanan).
    extra: pares clave/valor adicionales (tags, artefactos).
    path: ruta alternativa del CSV (por defecto outputs/metrics.csv).
    """
    p = _metrics_path(path)
    _ensure_parent(p)

    flat_metrics = _flatten(dict(metrics))
    flat_extra = _flatten(dict(extra)) if extra else {}

    row = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
        "model": model_name,
        **flat_metrics,
        **flat_extra,
    }

    # Leer cabecera existente si existe
    existing_header: list[str] = []
    if p.exists():
        try:
            with p.open("r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                existing_header = next(reader)
        except Exception:
            existing_header = []

    # Determinar nueva cabecera (unión preservando orden)
    base_cols = ["timestamp", "model"]
    metric_cols = sorted([c for c in row.keys() if c not in base_cols])
    header = base_cols + metric_cols

    # Unificar con header anterior si había
    if existing_header:
        # Añadir cualquier nuevo campo al final
        for col in header:
            if col not in existing_header:
                existing_header.append(col)
        header = existing_header

    # Asegurar que todas las claves existen en row
    for col in header:
        if col not in row:
            row[col] = ""

    write_header = not p.exists() or not existing_header
    with p.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    return p


__all__ = ["log_metrics"]
