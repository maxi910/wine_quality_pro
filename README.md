## Proyecto: Predicción / Análisis de Calidad de Vinos

Repositorio para explorar y modelar el dataset público de calidad de vinos (Wine Quality Data Set - UCI Machine Learning Repository).

### Estructura del proyecto

```
├── data/
│   ├── raw/                # Datos originales (no modificar manualmente)
│   └── processed/          # Datos procesados / features
├── notebooks/              # Exploración y EDA
├── src/
│   └── wine_quality/       # Código del paquete
├── tests/                  # Pruebas unitarias
├── outputs/                # Modelos entrenados / reportes
├── requirements.txt        # Dependencias principales
└── .github/workflows       # CI (GitHub Actions)
```

### Instalación rápida

```bash
python -m venv .venv
source .venv/bin/activate  # En macOS / Linux
pip install -r requirements.txt
```

### Uso del CLI

Se incluye un CLI mínimo usando Typer:

```bash
python -m wine_quality summary
```

Salida esperada: resumen de filas, columnas y conteo por tipo de vino.

### Desarrollo colaborativo

1. Haz fork o clona el repo:
   ```bash
   git clone https://github.com/<tu-org>/<repo>.git
   cd <repo>
   ```
2. Crea una rama descriptiva:
   ```bash
   git switch -c feature/nombre-claro
   ```
3. Ejecuta tests:
   ```bash
   pytest -q
   ```
4. Haz commits pequeños y claros.
5. Abre un Pull Request (PR) hacia `main`.

### Datos
Los archivos en `data/raw/` provienen del dataset público: Wine Quality (UCI). Referencia: https://archive.ics.uci.edu/ml/datasets/wine+quality

### Próximos pasos sugeridos
* Ingeniería de features en `features.py`.
* Pipelines de entrenamiento modulares en `src/wine_quality/models/`.
* Validación de esquema con `pandera` o `pydantic` (archivo `schema.py`).
* Añadir experiment tracking (MLflow / Weights & Biases) si se requiere.

### Arquitectura de modelos (refactor modular)

Los modelos se organizan ahora por archivos separados para escalabilidad:

```
src/wine_quality/models/
   base.py              # utilidades comunes (split, preprocesamiento, métricas, dataclass TrainResult)
   linear.py            # LinearRegression baseline
   random_forest.py     # RandomForestRegressor
   gradient_boosting.py # GradientBoostingRegressor
   xgboost_model.py     # XGBoost (import opcional)
   utils.py             # compare_models, tune_xgboost, save/load helpers
   __init__.py          # API consolidada del subpaquete (exporta funciones principales)
src/wine_quality/logging_utils.py  # logging ligero de métricas a outputs/metrics.csv
```

Puntos clave:
* Cada archivo expone una función `train_<modelo>` que devuelve `TrainResult`.
* `base.py` centraliza lógica repetida (evita duplicar preprocesamiento y métricas).
* El antiguo `model.py` quedó como fachada deprecada; será removido tras la transición (usa `from wine_quality import models` y luego `models.train_linear(...)`).

### Ejemplo de uso modular

```python
from wine_quality import load_wine_data, models

df = load_wine_data()
res = models.train_random_forest(df)
print(res.metrics)
```

### Logging de métricas

Cada comando CLI ahora registra métricas en `outputs/metrics.csv` para facilitar la comparación histórica.
Formato: timestamp, model, métricas y columnas extra (p.ej. artifact, tag).
* CLI (Typer) apunta ya a los módulos individuales para mayor claridad.

Ejemplo rápido en notebook:
```python
from wine_quality.data_io import load_wine_data
from wine_quality.models.random_forest import train_random_forest

df = load_wine_data()
res = train_random_forest(df, n_estimators=500)
res.metrics
```

Comparación de modelos (requiere funciones auxiliares todavía en transición):
```bash
python -m wine_quality.cli compare
```

Guardado de un modelo:
```bash
python -m wine_quality.cli save --model rf --path models/rf.joblib
```

Nota: Para XGBoost en macOS asegúrate de tener `libomp` instalado (`brew install libomp`).

### Licencia
Este proyecto se distribuye bajo licencia MIT (ver `LICENSE`).

### Contribuir
Lee `CONTRIBUTING.md` para estilo y flujo de trabajo.

---

Siéntete libre de abrir issues para mejoras o dudas.

```bash
python -m wine_quality.cli rf --n-estimators 200
```
