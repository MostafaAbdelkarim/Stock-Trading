from fastapi.testclient import TestClient
from ..routers import stock

client = TestClient(stock.router)


def test_create_user():
    response = client.get(
        "/CIB",
    )
    assert response.status_code == 200
