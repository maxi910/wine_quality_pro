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
* Pipeline de entrenamiento y evaluación en `model.py`.
* Validación de esquema con `pandera` o `pydantic` (archivo `schema.py`).
* Añadir experiment tracking (MLflow / Weights & Biases) si se requiere.

### Licencia
Este proyecto se distribuye bajo licencia MIT (ver `LICENSE`).

### Contribuir
Lee `CONTRIBUTING.md` para estilo y flujo de trabajo.

---

Siéntete libre de abrir issues para mejoras o dudas.
