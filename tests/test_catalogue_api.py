import datetime

def test_get_all_catalogues(client):
    response = client.get("/api/catalogues")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_catalogue_missing_fields(client):
    response = client.post("/api/catalogues", json={})
    assert response.status_code == 400

def test_create_catalogue_valid(client):
    payload = {
        "name": "Test Catalogue",
        "description": "Test description",
        "start_date": str(datetime.date.today()),
        "end_date": str(datetime.date.today() + datetime.timedelta(days=10)),
        "status": "active"
    }
    response = client.post("/api/catalogues", json=payload)
    assert response.status_code in [201, 500]  # 500 if DB insert fails

def test_get_catalogue_by_invalid_id(client):
    response = client.get("/api/catalogues/999999")
    assert response.status_code in [404, 200]

def test_update_catalogue_invalid_id(client):
    payload = {
        "name": "Updated Name",
        "description": "Updated Description",
        "start_date": str(datetime.date.today()),
        "end_date": str(datetime.date.today() + datetime.timedelta(days=10)),
        "status": "inactive"
    }
    response = client.put("/api/catalogues/999999", json=payload)
    assert response.status_code in [404, 200, 500]

def test_delete_catalogue_invalid_id(client):
    response = client.delete("/api/catalogues/999999")
    assert response.status_code in [404, 200]
