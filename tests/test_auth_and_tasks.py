import pytest

async def get_token(client):
    # signup
    r = await client.post("/auth/signup", json={"email":"a@test.com","password":"123456"})
    assert r.status_code in (200,201)
    token = r.json()["access_token"]
    return token

@pytest.mark.asyncio
async def test_create_and_list_tasks(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    # create
    r = await client.post("/tasks", json={"title":"Primera","description":"Desc"}, headers=headers)
    assert r.status_code == 201
    tid = r.json()["id"]
    # list
    r = await client.get("/tasks?limit=10&offset=0", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1
    # get
    r = await client.get(f"/tasks/{tid}", headers=headers)
    assert r.status_code == 200
    # update
    r = await client.put(f"/tasks/{tid}", json={"status":"completed"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "completed"
    # delete
    r = await client.delete(f"/tasks/{tid}", headers=headers)
    assert r.status_code == 204
    # get missing
    r = await client.get(f"/tasks/{tid}", headers=headers)
    assert r.status_code == 404
