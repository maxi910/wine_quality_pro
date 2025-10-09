import pytest
from wine_quality import load_wine_data, models

@pytest.mark.skipif(not models._XGB_AVAILABLE, reason="XGBoost no instalado")
def test_train_xgboost():
    df = load_wine_data()
    result = models.train_xgboost(df, n_estimators=50, test_size=0.3, random_state=0)
    assert 'rmse' in result.metrics
    assert result.metrics['rmse'] > 0
