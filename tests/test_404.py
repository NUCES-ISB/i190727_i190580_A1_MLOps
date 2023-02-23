import json


def test_404(app, client):
    print("IDHR AA GYA")
    res = client.get('/')
    print(res.status_code + " MY STATUS CODE")
    assert res.status_code == 200
    expected = {'errorCode' : 404, 'message' : 'Route not found'}
    print(json.loads(res.get_data(as_text=True)))
    assert expected == json.loads(res.get_data(as_text=True))
