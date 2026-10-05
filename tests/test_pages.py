def test_home_page_loads(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"QA Tracker" in r.data


def test_add_bug_from_form(client):
    r = client.post("/add", data={"title": "Form bug", "severity": "Low"}, follow_redirects=True)
    assert b"Form bug" in r.data


def test_form_rejects_blank_title(client):
    r = client.post("/add", data={"title": "  ", "severity": "Low"}, follow_redirects=True)
    assert b"No bugs found." in r.data


def test_delete_from_form(client):
    client.post("/add", data={"title": "Temp", "severity": "Low"})
    r = client.post("/delete/1", follow_redirects=True)
    assert b"Temp" not in r.data


def test_dashboard_counts(client):
    client.post("/api/bugs", json={"title": "A", "severity": "High"})
    r = client.get("/dashboard")
    assert r.status_code == 200
    assert b"Total bugs:</b> 1" in r.data
