from wine_quality import load_wine_data, models

def test_train_random_forest():
    df = load_wine_data()
    result = models.train_random_forest(df, n_estimators=50, test_size=0.3, random_state=0)
    assert 'rmse' in result.metrics
    assert result.metrics['rmse'] > 0
