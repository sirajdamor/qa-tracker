# QA Tracker
A web app to log bugs and manage test cases, built with Flask and tested with Pytest.

## Features
- Add, edit, delete and filter bugs by severity and status
- Manage test cases
- Dashboard with bug counts
- REST API for bugs

## Tech Stack
Python, Flask, SQLite, SQLAlchemy, Pytest

## Run locally
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py

## Run tests
pytest --cov=app