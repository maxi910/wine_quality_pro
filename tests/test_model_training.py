import pytest
from wine_quality import load_wine_data, models


def test_train_baseline_runs():
    df = load_wine_data()
    result = models.train_linear(df, test_size=0.25, random_state=123)
    # Verificamos que devuelve métricas esperadas
    assert 'rmse' in result.metrics
    assert 'mae' in result.metrics
    assert 'r2' in result.metrics
    # RMSE no debería ser cero y debe ser razonable (>0)
    assert result.metrics['rmse'] > 0
    # Modelo entrenado debe tener atributo predict
    assert hasattr(result.model, 'predict')
