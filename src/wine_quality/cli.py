"""CLI del proyecto usando Typer."""
from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from .data_io import load_wine_data

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


if __name__ == "__main__":  # pragma: no cover
	app()
