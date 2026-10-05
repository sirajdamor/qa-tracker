from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from . import db
from .models import Bug
from .services import SEVERITIES, STATUSES, count_by, validate_bug

bp = Blueprint("main", __name__)


# ---------- Web pages ----------
@bp.get("/")
def home():
    query = Bug.query
    status = request.args.get("status")
    severity = request.args.get("severity")
    if status:
        query = query.filter_by(status=status)
    if severity:
        query = query.filter_by(severity=severity)
    return render_template(
        "bugs.html",
        bugs=query.order_by(Bug.id.desc()).all(),
        severities=sorted(SEVERITIES),
        statuses=sorted(STATUSES),
    )


@bp.post("/add")
def add_bug_form():
    data = {
        "title": request.form.get("title", ""),
        "description": request.form.get("description", ""),
        "severity": request.form.get("severity", "Medium"),
    }
    if not validate_bug(data):
        db.session.add(Bug(**data))
        db.session.commit()
    return redirect(url_for("main.home"))


@bp.post("/delete/<int:bug_id>")
def delete_bug_form(bug_id):
    bug = db.session.get(Bug, bug_id)
    if bug:
        db.session.delete(bug)
        db.session.commit()
    return redirect(url_for("main.home"))


@bp.get("/dashboard")
def dashboard():
    bugs = Bug.query.all()
    return render_template(
        "dashboard.html",
        total=len(bugs),
        by_status=count_by(bugs, "status"),
        by_severity=count_by(bugs, "severity"),
    )


# ---------- REST API ----------
@bp.get("/api/bugs")
def list_bugs():
    query = Bug.query
    if request.args.get("status"):
        query = query.filter_by(status=request.args["status"])
    if request.args.get("severity"):
        query = query.filter_by(severity=request.args["severity"])
    return jsonify([b.to_dict() for b in query.all()])


@bp.post("/api/bugs")
def create_bug():
    data = request.get_json(silent=True) or {}
    errors = validate_bug(data)
    if errors:
        return jsonify({"errors": errors}), 400
    bug = Bug(
        title=data["title"].strip(),
        description=data.get("description", ""),
        severity=data.get("severity", "Medium"),
        status=data.get("status", "Open"),
    )
    db.session.add(bug)
    db.session.commit()
    return jsonify(bug.to_dict()), 201


@bp.get("/api/bugs/<int:bug_id>")
def get_bug(bug_id):
    bug = db.session.get(Bug, bug_id)
    if not bug:
        return jsonify({"error": "bug not found"}), 404
    return jsonify(bug.to_dict())


@bp.put("/api/bugs/<int:bug_id>")
def update_bug(bug_id):
    bug = db.session.get(Bug, bug_id)
    if not bug:
        return jsonify({"error": "bug not found"}), 404
    data = request.get_json(silent=True) or {}
    errors = validate_bug(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400
    for field in ("title", "description", "severity", "status"):
        if field in data:
            setattr(bug, field, data[field])
    db.session.commit()
    return jsonify(bug.to_dict())


@bp.delete("/api/bugs/<int:bug_id>")
def delete_bug(bug_id):
    bug = db.session.get(Bug, bug_id)
    if not bug:
        return jsonify({"error": "bug not found"}), 404
    db.session.delete(bug)
    db.session.commit()
    return "", 204
