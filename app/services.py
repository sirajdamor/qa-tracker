SEVERITIES = {"Low", "Medium", "High", "Critical"}
STATUSES = {"Open", "In Progress", "Resolved", "Closed"}


def validate_bug(data, partial=False):
    """Return a list of error messages. Empty list means the data is valid."""
    errors = []
    if not partial or "title" in data:
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append("title is required")
        elif len(title) > 120:
            errors.append("title must be 120 characters or less")
    if data.get("severity", "Medium") not in SEVERITIES:
        errors.append("invalid severity")
    if data.get("status", "Open") not in STATUSES:
        errors.append("invalid status")
    return errors


def count_by(bugs, field):
    """Count bugs by a field name, e.g. 'status' or 'severity'."""
    counts = {}
    for bug in bugs:
        value = getattr(bug, field)
        counts[value] = counts.get(value, 0) + 1
    return counts
