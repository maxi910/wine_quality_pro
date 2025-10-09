"""CLI del proyecto usando Typer."""
from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from .data_io import load_wine_data
from .models.linear import train_linear
from .models.random_forest import train_random_forest
from .models.gradient_boosting import train_gradient_boosting
from .models.xgboost_model import train_xgboost, _XGB_AVAILABLE
from .models.utils import (
	tune_xgboost,
	compare_models,
	save_model,
)
from .logging_utils import log_metrics

app = typer.Typer(help="Herramientas para explorar el dataset de calidad de vinos")
console = Console()


@app.command()
def summary() -> None:
	"""Muestra un resumen rápido del dataset combinado."""
	df = load_wine_data()
	table = Table(title="Resumen dataset vinos")
	table.add_column("Métrica", style="cyan")
	table.add_column("Valor", style="magenta")

	table.add_row("Filas", str(len(df)))
	table.add_row("Columnas", str(len(df.columns)))
	table.add_row("Tipos de vino", ", ".join(df["wine_type"].unique()))
	table.add_row("Calidad min-max", f"{df['quality'].min()} - {df['quality'].max()}")
	console.print(table)


@app.command()
def head(n: int = typer.Option(5, help="Número de filas a mostrar")) -> None:
	"""Muestra las primeras n filas."""
	df = load_wine_data()
	console.print(df.head(n))


@app.command()
def train(test_size: float = typer.Option(0.2, help="Proporción para test split (0-1)")) -> None:
	"""Entrena el modelo baseline (regresión lineal) y muestra métricas."""
	df = load_wine_data()
	result = train_linear(df, test_size=test_size)
	console.rule("Resultados entrenamiento (Baseline LinearRegression)")
	for k, v in result.metrics.items():
		console.print(f"[bold]{k.upper()}[/]: {v:.4f}")
	console.print(f"Filas test: {len(result.X_test)}")
	log_metrics("linear", result.metrics)


@app.command()
def rf(
	test_size: float = typer.Option(0.2, help="Proporción para test split"),
	n_estimators: int = typer.Option(400, help="Número de árboles"),
	max_depth: int = typer.Option(None, help="Profundidad máxima (None = ilimitado)"),
	random_state: int = typer.Option(42, help="Semilla"),
	n_jobs: int = typer.Option(-1, help="Paralelismo (-1 = todos los cores)"),
) -> None:
	"""Entrena un RandomForestRegressor y muestra métricas."""
	df = load_wine_data()
	result = train_random_forest(
		df,
		n_estimators=n_estimators,
		max_depth=max_depth if max_depth is not None else None,
		test_size=test_size,
		random_state=random_state,
		n_jobs=n_jobs,
	)
	console.rule("Resultados entrenamiento (RandomForestRegressor)")
	for k, v in result.metrics.items():
		console.print(f"[bold]{k.upper()}[/]: {v:.4f}")
	console.print(f"Filas test: {len(result.X_test)}")
	log_metrics("random_forest", result.metrics)


@app.command()
def gbr(
	test_size: float = typer.Option(0.2, help="Proporción para test split"),
	n_estimators: int = typer.Option(300, help="Número de árboles (stages)") ,
	learning_rate: float = typer.Option(0.1, help="Learning rate"),
	max_depth: int = typer.Option(3, help="Profundidad de los árboles base"),
	subsample: float = typer.Option(1.0, help="Subsample para stochastic boosting (<=1.0)"),
	random_state: int = typer.Option(42, help="Semilla"),
) -> None:
	"""Entrena un GradientBoostingRegressor."""
	df = load_wine_data()
	result = train_gradient_boosting(
		df,
		n_estimators=n_estimators,
		learning_rate=learning_rate,
		max_depth=max_depth,
		subsample=subsample,
		test_size=test_size,
		random_state=random_state,
	)
	console.rule("Resultados entrenamiento (GradientBoostingRegressor)")
	for k, v in result.metrics.items():
		console.print(f"[bold]{k.upper()}[/]: {v:.4f}")
	console.print(f"Filas test: {len(result.X_test)}")
	log_metrics("gradient_boosting", result.metrics)


@app.command()
def xgb(
	test_size: float = typer.Option(0.2, help="Proporción test"),
	n_estimators: int = typer.Option(500, help="Número de árboles"),
	learning_rate: float = typer.Option(0.05, help="Learning rate"),
	max_depth: int = typer.Option(6, help="Profundidad máxima"),
	subsample: float = typer.Option(0.8, help="Subsample"),
	colsample_bytree: float = typer.Option(0.8, help="Fracción de columnas"),
	reg_lambda: float = typer.Option(1.0, help="L2 regularization"),
	reg_alpha: float = typer.Option(0.0, help="L1 regularization"),
	random_state: int = typer.Option(42, help="Semilla"),
	n_jobs: int = typer.Option(-1, help="Hilos paralelos"),
) -> None:
	"""Entrena un XGBoost Regressor (si está instalado)."""
	df = load_wine_data()
	if not _XGB_AVAILABLE:
		console.print("[yellow]XGBoost no disponible. Instala 'xgboost' para usar este comando.[/]")
		return
	result = train_xgboost(
		df,
		n_estimators=n_estimators,
		learning_rate=learning_rate,
		max_depth=max_depth,
		subsample=subsample,
		colsample_bytree=colsample_bytree,
		reg_lambda=reg_lambda,
		reg_alpha=reg_alpha,
		test_size=test_size,
		random_state=random_state,
		n_jobs=n_jobs,
	)
	console.rule("Resultados entrenamiento (XGBRegressor)")
	for k, v in result.metrics.items():
		console.print(f"[bold]{k.upper()}[/]: {v:.4f}")
	console.print(f"Filas test: {len(result.X_test)}")
	log_metrics("xgboost", result.metrics)


@app.command()
def xgb_tune(
	n_iter: int = typer.Option(20, help="Iteraciones RandomizedSearch"),
	cv: int = typer.Option(5, help="Folds CV"),
	early_stopping_rounds: int = typer.Option(30, help="Early stopping rounds"),
	test_size: float = typer.Option(0.2, help="Proporción test"),
	random_state: int = typer.Option(42, help="Semilla"),
	n_jobs: int = typer.Option(-1, help="Paralelismo"),
) -> None:
	"""Ejecuta un RandomizedSearchCV para XGBoost y muestra mejores parámetros."""
	df = load_wine_data()
	try:
		result = tune_xgboost(
			df,
			n_iter=n_iter,
			cv=cv,
			early_stopping_rounds=early_stopping_rounds,
			test_size=test_size,
			random_state=random_state,
			n_jobs=n_jobs,
		)
	except RuntimeError as e:
		console.print(f"[red]Error:[/] {e}")
		return
	console.rule("Resultados tuning XGBoost (mejor modelo)")
	for k, v in result.metrics.items():
		if k == "best_params":
			console.print("[bold]BEST_PARAMS[/]:")
			for pk, pv in v.items():
				console.print(f"  - {pk}: {pv}")
		else:
			console.print(f"[bold]{k.upper()}[/]: {v:.4f}")
	console.print(f"Filas test: {len(result.X_test)}")
	log_metrics("xgboost_tuned", {k: v for k, v in result.metrics.items() if k != "best_params"}, extra={"tag": "tuned"})


@app.command()
def compare(include_xgb: bool = typer.Option(True, help="Incluir XGBoost si está disponible")) -> None:
	"""Compara modelos (Linear, RF, GBR, XGB) y muestra métricas."""
	df = load_wine_data()
	try:
		results = compare_models(df, include_xgb=include_xgb)
	except RuntimeError as e:
		console.print(f"[red]Error:[/] {e}")
		return
	table = Table(title="Comparación de Modelos (ordenado por RMSE)")
	for col in results.columns:
		table.add_column(col.upper())
	for _, row in results.iterrows():
		vals = [f"{row[c]:.4f}" if c != "model" else str(row[c]) for c in results.columns]
		table.add_row(*vals)
	console.print(table)


@app.command()
def save(
    model: str = typer.Option("linear", help="Modelo a entrenar: linear|rf|gbr|xgb"),
    path: str = typer.Option("models/model.joblib", help="Ruta de salida"),
) -> None:
    """Entrena un modelo seleccionado (usando módulos nuevos) y lo guarda en disco."""
    df = load_wine_data()
    model_key = model.lower()
    if model_key == "linear":
        res = train_linear(df)
    elif model_key == "rf":
        res = train_random_forest(df)
    elif model_key == "gbr":
        res = train_gradient_boosting(df)
    elif model_key == "xgb":
        if not _XGB_AVAILABLE:
            console.print("[yellow]XGBoost no disponible. Instala 'xgboost'.[/]")
            return
        res = train_xgboost(df)
    else:
        console.print("[red]Modelo no reconocido[/]")
        return
    save_model(res.model, path)
    log_metrics(f"{model_key}_saved", res.metrics, extra={"artifact": path})
    console.print(f"[green]Modelo guardado en[/] {path}")


if __name__ == "__main__":  # pragma: no cover
	app()

