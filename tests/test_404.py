import json

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = {'errorCode' : 404, 'message' : 'Route not found'}
    assert expected == json.loads(res.get_data(as_text=True))