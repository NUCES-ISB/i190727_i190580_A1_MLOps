import pytest
from app import app as flask_app
@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_404(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = {'errorCode' : 404, 'message' : 'Route not found'}
    assert expected == json.loads(res.get_data(as_text=True))