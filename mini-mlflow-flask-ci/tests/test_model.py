# tests/test_model.py
from train import train_and_log
from sklearn.linear_model import LinearRegression

def test_train_returns_model():
    model = train_and_log()
    assert isinstance(model, LinearRegression)
    # simple smoke test for prediction
    pred = model.predict([[4]])
    assert pred.shape == (1,)