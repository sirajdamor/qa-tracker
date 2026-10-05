def make_bug(client, **overrides):
    payload = {"title": "Login fails", "severity": "High"}
    payload.update(overrides)
    return client.post("/api/bugs", json=payload)


def test_create_bug(client):
    r = make_bug(client)
    assert r.status_code == 201
    assert r.get_json()["title"] == "Login fails"
    assert r.get_json()["status"] == "Open"


def test_create_bug_missing_title(client):
    r = client.post("/api/bugs", json={"severity": "Low"})
    assert r.status_code == 400


def test_create_bug_invalid_severity(client):
    assert make_bug(client, severity="Huge").status_code == 400


def test_create_bug_without_json(client):
    assert client.post("/api/bugs").status_code == 400


def test_get_bug(client):
    bug_id = make_bug(client).get_json()["id"]
    r = client.get(f"/api/bugs/{bug_id}")
    assert r.status_code == 200
    assert r.get_json()["id"] == bug_id


def test_get_bug_not_found(client):
    assert client.get("/api/bugs/999").status_code == 404


def test_list_bugs(client):
    make_bug(client, title="A")
    make_bug(client, title="B")
    assert len(client.get("/api/bugs").get_json()) == 2


def test_filter_by_status(client):
    make_bug(client, title="A", status="Open")
    make_bug(client, title="B", status="Closed")
    r = client.get("/api/bugs?status=Closed")
    assert [b["title"] for b in r.get_json()] == ["B"]


def test_filter_by_severity(client):
    make_bug(client, title="A", severity="Low")
    make_bug(client, title="B", severity="Critical")
    r = client.get("/api/bugs?severity=Critical")
    assert [b["title"] for b in r.get_json()] == ["B"]


def test_update_bug(client):
    bug_id = make_bug(client).get_json()["id"]
    r = client.put(f"/api/bugs/{bug_id}", json={"status": "Resolved"})
    assert r.status_code == 200
    assert r.get_json()["status"] == "Resolved"


def test_update_bug_invalid_status(client):
    bug_id = make_bug(client).get_json()["id"]
    assert client.put(f"/api/bugs/{bug_id}", json={"status": "Done"}).status_code == 400


def test_update_bug_not_found(client):
    assert client.put("/api/bugs/999", json={"status": "Closed"}).status_code == 404


def test_delete_bug(client):
    bug_id = make_bug(client).get_json()["id"]
    assert client.delete(f"/api/bugs/{bug_id}").status_code == 204
    assert client.get(f"/api/bugs/{bug_id}").status_code == 404


def test_delete_bug_not_found(client):
    assert client.delete("/api/bugs/999").status_code == 404
