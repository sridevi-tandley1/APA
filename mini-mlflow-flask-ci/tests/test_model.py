import pandas as pd
from sklearn.linear_model import LinearRegression

from train import FEATURES, train_and_log


def test_train_returns_model():
    model = train_and_log()
    assert isinstance(model, LinearRegression)
    pred = model.predict(pd.DataFrame([[4]], columns=FEATURES))
    assert pred.shape == (1,)
    # quality gate: more experience should never predict a lower salary
    assert model.coef_[0] > 0
