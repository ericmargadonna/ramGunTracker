import pytest
from flask import g, session
from ramApp.db import get_db




def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register', data={'username':'a', 'password':'a', 'key':'dev'})
    assert response.headers['Location'] == '/auth/login'

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM USER WHERE NAME = 'a'"
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'key', 'message'), (
    ('', '', '', b'Username is required.'),
    ('a', '', '', b'Password is required.'),
    ('a', 'a', '', b'Registration key required.'),
    ('a', 'a', 'a', b'Incorrect registration key provided.'),
    ('test', 'test', 'dev', b'already registered'),
))
def test_register_validate_input(client, username, password, key, message):
    response = client.post(
        '/auth/register',
        data={'username':username, 'password':password, 'key':key}
    )
    assert message in response.data




def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == '/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['NAME'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data