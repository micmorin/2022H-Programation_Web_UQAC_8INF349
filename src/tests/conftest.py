import pytest
from main.app import create_app
from main.app_init.database import db
from flask_login import current_user, user_logged_in

@pytest.fixture()
def app():
    return create_app()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def clientLecteur(client):
    client.post('/login', data={'username':'lecteur', 'password':'lecteur'}, follow_redirects=True)
    return client

@pytest.fixture()
def clientAuteur(client):
    client.post('/login', data={'username':'auteur', 'password':'auteur'}, follow_redirects=True)
    return client

@pytest.fixture()
def clientAdmin(client):
    client.post('/login', data={'username':'admin', 'password':'admin'}, follow_redirects=True)
    return client


# @pytest.fixture(scope='module')
# def init_database():
#     app = create_app()
#     client = app.test_client()
#     with app.app_context:
#         user = User(username="foobar", email="foo@bar.com")
#         db.session.add(user)
#         db.session.commit()
#     yield db
#     db.session.close()

