import pytest

from train import train_and_log


@pytest.fixture(scope="module")
def client():
    train_and_log()  # make sure a registered model exists
    import app as app_module
    app_module.model = None
    return app_module.app.test_client()


def test_health(client):
    assert client.get("/health").status_code == 200


def test_single_and_batch_predictions(client):
    one = client.post("/predict", json={"experience_years": 4})
    many = client.post("/predict", json={"instances": [[2], [5], [8]]})
    assert one.status_code == 200 and len(one.get_json()["predictions"]) == 1
    assert many.status_code == 200 and len(many.get_json()["predictions"]) == 3


def test_bad_input_returns_json_400(client):
    assert client.post("/predict", data="x").status_code == 400
    assert client.post("/predict", json={"foo": 1}).status_code == 400
    assert client.post("/predict", json={"instances": [["abc"]]}).status_code == 400
