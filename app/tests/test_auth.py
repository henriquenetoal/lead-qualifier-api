def test_register_user(client):
    response = client.post("/register", json={
        "username": "teste_user",
        "password": "senha123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_lead_without_token_fails(client):
    response = client.post("/leads", json={
        "name": "Lead Sem Token",
        "email": "semtoken@teste.com"
    })

    assert response.status_code == 401

def test_full_flow_create_lead_with_token(client):
    client.post("/register", json={
        "username": "vendedor1",
        "password": "senha123"
    })

    login_response = client.post("/login", data={
        "username": "vendedor1",
        "password": "senha123"
    })
    token = login_response.json()["access_token"]

    response = client.post(
        "/leads",
        json={"name": "Cliente Teste", "email": "cliente@teste.com"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Cliente Teste"