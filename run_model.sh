#!/usr/bin/env bash
# Script unificado para correr el código del proyecto (entrenar modelos y ver métricas)
# Uso básico:
#   bash run_model.sh            # ejecuta flujo por defecto
#   bash run_model.sh --no-xgb   # omite XGBoost
#   bash run_model.sh --tune-xgb # incluye tuning de XGBoost
#   bash run_model.sh --help

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_ROOT/../.venv"
REQ_FILE="$PROJECT_ROOT/requirements.txt"
PYTHON_BIN="python"

NO_XGB=false
DO_TUNE_XGB=false
QUIET=false

print_help() {
  cat <<EOF
Script para ejecutar el flujo de entrenamiento de modelos de calidad de vinos.

Opciones:
  --no-xgb       Omite entrenamiento y comparación con XGBoost
  --tune-xgb     Ejecuta tuning (RandomizedSearchCV) de XGBoost después del resto
  --quiet        Reduce la salida (solo pasos clave)
  --help         Muestra esta ayuda

Flujo por defecto:
  1. Crear / activar entorno virtual (si no existe)
  2. Instalar dependencias (solo si falta algo esencial)
  3. Entrenar: linear, random forest, gradient boosting
  4. Entrenar XGBoost (si disponible y no se desactiva)
  5. Comparar modelos
  6. Mostrar últimas filas de outputs/metrics.csv

Resultados:
  - Métricas acumuladas en outputs/metrics.csv
  - Modelos guardados solo si se invoca manualmente 'save' (no por defecto aquí)
EOF
}

log() { $QUIET && return 0; echo -e "[run_model] $*"; }

ensure_venv() {
  if [ ! -d "$VENV_DIR" ]; then
    log "Creando entorno virtual en $VENV_DIR";
    python -m venv "$VENV_DIR";
  fi
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  PYTHON_BIN="$(command -v python)"
}

needs_install() {
  # Devuelve 0 (true) si falta algún import clave
  "$PYTHON_BIN" - <<'PY' >/dev/null 2>&1
import importlib, sys
mods = ["pandas","sklearn","typer","rich"]
missing = [m for m in mods if importlib.util.find_spec(m) is None]
if missing:
    sys.exit(1)
PY
  local status=$?
  if [ $status -ne 0 ]; then
    return 0  # necesita instalar
  fi
  return 1  # no necesita instalar
}

install_requirements() {
  if needs_install; then
    log "Instalando dependencias (requirements.txt)";
    "$PYTHON_BIN" -m pip install -r "$REQ_FILE"
  else
    log "Dependencias básicas ya presentes (skip install)";
  fi
}

run_cli() {
  local cmd=("$PYTHON_BIN" -m wine_quality.cli "$@")
  log "> ${cmd[*]}"
  "${cmd[@]}"
}

train_sequence() {
  log "Entrenando LinearRegression..."; run_cli train || true
  log "Entrenando RandomForest..."; run_cli rf --n-estimators 300 || true
  log "Entrenando GradientBoosting..."; run_cli gbr --n-estimators 300 --learning-rate 0.1 || true
  if ! $NO_XGB; then
    log "Entrenando XGBoost (si disponible)..."; run_cli xgb || true
  fi
}

compare_models() {
  if $NO_XGB; then
    log "Comparando modelos sin XGBoost"; run_cli compare --include-xgb False || true
  else
    log "Comparando modelos (incluyendo XGBoost si está)"; run_cli compare || true
  fi
}

tune_xgb() {
  if $DO_TUNE_XGB; then
    if $NO_XGB; then
      log "--tune-xgb ignorado porque --no-xgb está activo";
    else
      log "Ejecutando tuning de XGBoost..."; run_cli xgb_tune --n-iter 15 --cv 5 || true
    fi
  fi
}

show_metrics_tail() {
  local metrics_file="$PROJECT_ROOT/outputs/metrics.csv"
  if [ -f "$metrics_file" ]; then
    log "Últimas métricas registradas:";
    awk 'NR==1 || NR>1 {print}' "$metrics_file" | tail -n 10
  else
    log "No existe todavía outputs/metrics.csv (¿falló todo el entrenamiento?)";
  fi
}

parse_args() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --no-xgb) NO_XGB=true ; shift ;;
      --tune-xgb) DO_TUNE_XGB=true ; shift ;;
      --quiet) QUIET=true ; shift ;;
      --help|-h) print_help; exit 0 ;;
      *) echo "Argumento desconocido: $1"; exit 1 ;;
    esac
  done
}

main() {
  parse_args "$@"
  log "Usando raíz de proyecto: $PROJECT_ROOT"
  log "Verificando/creando entorno virtual..."
  ensure_venv
  log "Python en uso: $(command -v python)"
  log "Instalando dependencias si es necesario..."
  install_requirements
  # Asegurar que PYTHONPATH no cause 'unbound variable' con set -u
  export PYTHONPATH="$PROJECT_ROOT/src:${PYTHONPATH:-}"
  log "PYTHONPATH=$PYTHONPATH"
  # Crear carpeta de outputs si no existe
  mkdir -p "$PROJECT_ROOT/outputs"
  log "Secuencia de entrenamiento..."
  train_sequence
  log "Comparando modelos..."
  compare_models
  log "Tuning (si aplica)..."
  tune_xgb
  log "Mostrando últimas métricas..."
  show_metrics_tail
  log "Flujo completo terminado. Archivo de métricas: outputs/metrics.csv"
}

main "$@"
