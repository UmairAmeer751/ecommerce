import pytest
import sys
import os

# Make backend importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app, db


@pytest.fixture(scope='module')
def client():
    """Create a test Flask client backed by an in-memory SQLite DB."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


# ── Test 1: Health endpoint ──────────────────────────────────
def test_health_endpoint_returns_200(client):
    response = client.get('/api/health')
    assert response.status_code == 200


def test_health_endpoint_returns_json(client):
    response = client.get('/api/health')
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'ecommerce-backend'


# ── Test 2: Products endpoint ────────────────────────────────
def test_products_endpoint_returns_200(client):
    response = client.get('/api/products')
    assert response.status_code == 200


def test_products_returns_list(client):
    response = client.get('/api/products')
    data = response.get_json()
    assert isinstance(data, list)


# ── Test 3: Unknown route returns 404 ────────────────────────
def test_unknown_route_returns_404(client):
    response = client.get('/api/does-not-exist')
    assert response.status_code == 404
