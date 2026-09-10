import pytest

from app import create_app
from constants import ROLE_ADMIN, ROLE_GENERAL, ROLE_GOLD
from extensions import db
from models import User
from werkzeug.security import generate_password_hash


class TestConfig:
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = 'test-secret-key-that-is-at-least-32-bytes-long'


@pytest.fixture()
def app():
  application = create_app(TestConfig)
  with application.app_context():
    db.create_all()
    yield application
    db.session.remove()
    db.drop_all()


@pytest.fixture()
def client(app):
  return app.test_client()


def register(client, username, password='pw', **extra):
  return client.post('/api/auth/register', json={
      'username': username, 'password': password, **extra,
  })


def login(client, username, password='pw'):
  response = client.post('/api/auth/login', json={
      'username': username, 'password': password,
  })
  return response.get_json()['access_token']


def auth(token):
  return {'Authorization': f'Bearer {token}'}


def create_user(app, username, role):
  with app.app_context():
    user = User(username=username, password=generate_password_hash('pw'), role=role)
    db.session.add(user)
    db.session.commit()
    return user.id


def test_register_always_creates_general_user(client, app):
  response = register(client, 'new-user', role=ROLE_ADMIN)
  assert response.status_code == 201
  with app.app_context():
    assert User.query.filter_by(username='new-user').one().role == ROLE_GENERAL


@pytest.mark.parametrize(('role', 'gold_status', 'admin_status'), [
    (ROLE_GENERAL, 403, 403),
    (ROLE_GOLD, 200, 403),
    (ROLE_ADMIN, 200, 200),
])
def test_role_access_matrix(client, app, role, gold_status, admin_status):
  create_user(app, f'user-{role}', role)
  token = login(client, f'user-{role}')
  assert client.get('/api/gold/lounge', headers=auth(token)).status_code == gold_status
  assert client.get('/api/admin/users', headers=auth(token)).status_code == admin_status


def test_protected_api_requires_login(client):
  assert client.get('/api/gold/lounge').status_code == 401
  assert client.get('/api/admin/users').status_code == 401


def test_admin_can_promote_and_delete_user(client, app):
  create_user(app, 'admin', ROLE_ADMIN)
  target_id = create_user(app, 'member', ROLE_GENERAL)
  token = login(client, 'admin')

  updated = client.put(
      f'/api/admin/users/{target_id}', headers=auth(token), json={'role': ROLE_GOLD})
  assert updated.status_code == 200
  assert updated.get_json()['role'] == ROLE_GOLD

  member_token = login(client, 'member')
  assert client.get('/api/gold/lounge', headers=auth(member_token)).status_code == 200

  deleted = client.delete(f'/api/admin/users/{target_id}', headers=auth(token))
  assert deleted.status_code == 200
  with app.app_context():
    assert db.session.get(User, target_id) is None


def test_admin_cannot_delete_or_demote_self(client, app):
  admin_id = create_user(app, 'admin', ROLE_ADMIN)
  token = login(client, 'admin')
  assert client.delete(f'/api/admin/users/{admin_id}', headers=auth(token)).status_code == 400
  assert client.put(
      f'/api/admin/users/{admin_id}', headers=auth(token), json={'role': ROLE_GENERAL}
  ).status_code == 400


def test_role_change_is_effective_without_new_login(client, app):
  create_user(app, 'admin', ROLE_ADMIN)
  member_id = create_user(app, 'member', ROLE_GENERAL)
  admin_token = login(client, 'admin')
  member_token = login(client, 'member')

  assert client.get('/api/gold/lounge', headers=auth(member_token)).status_code == 403
  client.put(
      f'/api/admin/users/{member_id}', headers=auth(admin_token), json={'role': ROLE_GOLD})
  assert client.get('/api/gold/lounge', headers=auth(member_token)).status_code == 200


def test_page_routes_render(client):
  assert client.get('/').status_code == 200
  assert client.get('/gold').status_code == 200
  assert client.get('/admin').status_code == 200
