from ..util_func import response_json


def test_ping(client):
    res = client.get('ping')
    data = response_json(res)

    assert res.status_code == 200
    assert "pong" in data["message"]
    assert "success" in data["status"]

