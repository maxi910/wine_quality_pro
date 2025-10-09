## Guía Rápida: Cómo correr y ver métricas de los modelos

Este documento resume los pasos para ejecutar los modelos, comparar resultados, tunear hiperparámetros y consultar el histórico de métricas.

---

### 1. Preparar el entorno

Crear y activar entorno virtual (una sola vez):
```zsh
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
pip install -r requirements.txt
```

Instalación editable (opcional, facilita imports sin manipular rutas):
```zsh
pip install -e .
```

Verificar versión de Python dentro del entorno:
```zsh
python -V
```

---

### 2. Comandos CLI principales

Todos se ejecutan desde la raíz del proyecto (donde está este archivo y `README.md`).

Resumen del dataset:
```zsh
python -m wine_quality.cli summary
```

Primeras filas:
```zsh
python -m wine_quality.cli head --n 8
```

Entrenar baseline (LinearRegression):
```zsh
python -m wine_quality.cli train
```

Random Forest:
```zsh
python -m wine_quality.cli rf --n-estimators 400
```

Gradient Boosting:
```zsh
python -m wine_quality.cli gbr --n-estimators 300 --learning-rate 0.1
```

XGBoost (si está instalado y libomp disponible):
```zsh
python -m wine_quality.cli xgb
```

Tuning de XGBoost (RandomizedSearchCV + early stopping):
```zsh
python -m wine_quality.cli xgb_tune --n-iter 20 --cv 5
```

Comparar varios modelos (tabla ordenada por RMSE):
```zsh
python -m wine_quality.cli compare
```

Comparar sin XGBoost:
```zsh
python -m wine_quality.cli compare --include-xgb False
```

Guardar un modelo entrenado (ejemplo Random Forest):
```zsh
python -m wine_quality.cli save --model rf --path models/rf.joblib
```

Parámetros útiles (ejemplos):
```zsh
python -m wine_quality.cli rf --n-estimators 600 --max-depth 12
python -m wine_quality.cli gbr --n-estimators 400 --learning-rate 0.05 --subsample 0.8
python -m wine_quality.cli xgb --n-estimators 800 --learning-rate 0.05 --max-depth 7
```

---

### 3. Histórico de métricas

Cada ejecución de entrenamiento/tuning escribe (append) una fila en:
```
outputs/metrics.csv
```

Ver últimas filas:
```zsh
python - <<'PY'
import pandas as pd
df = pd.read_csv('outputs/metrics.csv')
print(df.tail())
PY
```

Columnas típicas:
* `timestamp` – fecha UTC
* `model` – nombre lógico (linear, random_forest, gradient_boosting, xgboost, xgboost_tuned, rf_saved, etc.)
* `rmse`, `mse`, `mae`, `r2`
* `artifact` – ruta del modelo si se usó `save`
* `tag` – por ejemplo `tuned` en tuning

Interpretación breve:
* RMSE (Root Mean Squared Error): error promedio en escala del objetivo.
* MAE: error absoluto medio, robusto a outliers.
* R²: proporción de varianza explicada (más cercano a 1 es mejor; puede ser negativo si el modelo es peor que un baseline).

---

### 4. Uso programático en Python

```zsh
python - <<'PY'
import sys, pathlib
src = pathlib.Path('src').resolve()
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

from wine_quality import load_wine_data, models

df = load_wine_data()
res = models.train_random_forest(df, n_estimators=200)
print('Métricas:', res.metrics)
PY
```

Resultado (`res.metrics`) es un dict con rmse, mse, mae, r2.

---

### 5. Troubleshooting común

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| `ModuleNotFoundError: wine_quality` | Paquete no instalado o falta `src` en PYTHONPATH | `pip install -e .` o asegurarse de ejecutar desde raíz con estructura intacta |
| XGBoost no aparece en compare | No instalado o falló import | `pip install xgboost` y en macOS: `brew install libomp` |
| Métricas no se registran | Falla de escritura en `outputs/` | Crear carpeta `mkdir -p outputs` y revisar permisos |
| RMSE muy alta | Parámetros poco óptimos | Probar tuning (`xgb_tune`) o ajustar hiperparámetros |

---

### 6. Siguientes mejoras sugeridas
1. Validación de esquema (pandera) antes de entrenar.
2. Feature engineering en `features.py`.
3. Cross-validation en `compare_models`.
4. Loggear también `best_params` completos en CSV de tuning.
5. Integración con MLflow / Weights & Biases.

---

### 7. Ejemplos rápidos combinados

Entrenar tres modelos y luego ver las últimas métricas:
```zsh
python -m wine_quality.cli train
python -m wine_quality.cli rf --n-estimators 300
python -m wine_quality.cli gbr --n-estimators 400 --learning-rate 0.05

python - <<'PY'
import pandas as pd
print(pd.read_csv('outputs/metrics.csv').tail(3))
PY
```

---

### 8. Limpieza / Repetibilidad
Reiniciar histórico de métricas (opcional):
```zsh
rm -f outputs/metrics.csv
```
Luego volver a correr entrenamientos.

---

### 9. Estructura relevante (resumen)
```
src/wine_quality/
  cli.py               # Comandos Typer
  data_io.py           # Carga y combinación de datasets
  logging_utils.py     # Registro de métricas CSV
  models/
    base.py            # Preprocesamiento y utilidades comunes
    linear.py          # Modelo baseline
    random_forest.py   # RandomForestRegressor
    gradient_boosting.py
    xgboost_model.py   # Modelo XGBoost opcional
    utils.py           # compare, tune, save/load
    __init__.py        # Reexporta API principal
```

---

### 10. Contacto / Colaboración
Usar PRs siguiendo la guía de workflow y revisar `outputs/metrics.csv` para monitorear regresiones de performance.

---

¿Necesitas que añadamos automatización (por ejemplo, un script `make compare`)? Pídelo y lo incorporamos.
