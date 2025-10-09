"""[DEPRECATED] Este módulo ha sido refactorizado.

Mantiene alias para compatibilidad retro; usar módulos en `wine_quality.models.*`.
"""
from __future__ import annotations

from warnings import warn

from .models.linear import train_linear as train  # noqa: F401
from .models.random_forest import train_random_forest  # noqa: F401
from .models.gradient_boosting import train_gradient_boosting  # noqa: F401
from .models.xgboost_model import train_xgboost  # noqa: F401
from .models.base import prepare_data, evaluate, TrainResult  # noqa: F401
from .models.utils import (
	tune_xgboost,  # noqa: F401
	compare_models,  # noqa: F401
	save_model,  # noqa: F401
	load_model,  # noqa: F401
)

warn(
	"'wine_quality.model' está deprecado; usa 'wine_quality.models.*'. Este proxy se eliminará en el futuro.",
	DeprecationWarning,
)

__all__ = [
	"train",
	"train_random_forest",
	"train_gradient_boosting",
	"train_xgboost",
	"tune_xgboost",
	"compare_models",
	"save_model",
	"load_model",
	"prepare_data",
	"evaluate",
	"TrainResult",
]

