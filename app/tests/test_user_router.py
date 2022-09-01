from fastapi.testclient import TestClient
from ..routers import user

client = TestClient(user.router)


def test_create_user():
    response = client.post(
        "/create",
        json={
            'first_name': 'Hamada',
            'last_name': 'Hamdy',
            'email': 'hamada@gmail.com',
            'password': '1122334455',
            'amount': 50}
    )
    assert response.status_code == 201


def test_deposite_user():
    response = client.put(
        '/deposite',
        json={
            'user_id': '259313fb-64be-4d2a-9c56-e3c5e753b073',
            'amount': 200
        }
    )
    assert response.status_code == 200


def test_deposite_user():
    response = client.put(
        '/withdraw',
        json={
            'user_id': '259313fb-64be-4d2a-9c56-e3c5e753b073',
            'amount': 200
        }
    )
    assert response.status_code == 200
