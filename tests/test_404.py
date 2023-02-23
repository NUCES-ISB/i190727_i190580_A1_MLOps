import json


def test_404(app, client):
    print("IDHR AA GYA")
    res = client.get('/404')
    print(f"MY STATUS CODE: {str(res.status_code)}")
    assert res.status_code == 200
    expected = {'errorCode' : 404, 'message' : 'Route not found'}
    print(1, res.get_data(as_text=True))
    print(2, json.loads(res.get_data(as_text=True)))
    assert expected == json.loads(res.get_data(as_text=True))
