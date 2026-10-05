from app.services import count_by, validate_bug


class FakeBug:
    def __init__(self, status, severity):
        self.status = status
        self.severity = severity


def test_valid_bug_has_no_errors():
    assert validate_bug({"title": "Crash on save", "severity": "High"}) == []


def test_missing_title():
    assert "title is required" in validate_bug({"severity": "Low"})


def test_blank_title():
    assert "title is required" in validate_bug({"title": "   "})


def test_title_too_long():
    assert "title must be 120 characters or less" in validate_bug({"title": "x" * 121})


def test_invalid_severity():
    assert "invalid severity" in validate_bug({"title": "a", "severity": "Huge"})


def test_invalid_status():
    assert "invalid status" in validate_bug({"title": "a", "status": "Done"})


def test_partial_update_allows_missing_title():
    assert validate_bug({"status": "Closed"}, partial=True) == []


def test_count_by_status():
    bugs = [FakeBug("Open", "Low"), FakeBug("Open", "High"), FakeBug("Closed", "Low")]
    assert count_by(bugs, "status") == {"Open": 2, "Closed": 1}


def test_count_by_empty_list():
    assert count_by([], "severity") == {}
