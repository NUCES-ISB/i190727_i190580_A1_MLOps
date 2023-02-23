import json


def test_404(app, client):
    res = client.get('/404')
    assert res.status_code == 200
    expected = {'errorCode' : 404, 'message' : 'Route not found'}
    assert expected == json.loads(res.get_data(as_text=True))
