from main.models.md_user import User

def test_app_is_created(app):
    assert app.name == 'main.app'

def test_config_is_loaded(app):
    assert app.config["DEBUG"] is True

def test_request_returns_404(client):
    assert client.get("/url_does_not_exists").status_code == 404

def test_request_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Home Page" in response.data

def test_login_lecteur(clientLecteur):
    with clientLecteur.session_transaction() as session:
        assert  User.query.filter(User.id == session['_user_id']).first().username == "lecteur"

def test_login_auteur(clientAuteur):

    with clientAuteur.session_transaction() as session:
        assert  User.query.filter(User.id == session['_user_id']).first().username == "auteur"

def test_login_admin(clientAdmin):
    with clientAdmin.session_transaction() as session:
        assert  User.query.filter(User.id == session['_user_id']).first().username == "admin"

def test_logout_lecteur(clientLecteur):
    with clientLecteur.session_transaction() as session:
        response = clientLecteur.get('/logout', follow_redirects=True)
        assert b"Register" in response.data

def test_logout_auteur(clientAuteur):

    with clientAuteur.session_transaction() as session:
        response = clientAuteur.get('/logout', follow_redirects=True)
        assert b"Register" in response.data

def test_logout_admin(clientAdmin):
    with clientAdmin.session_transaction() as session:
        response = clientAdmin.get('/logout', follow_redirects=True)
        assert b"Register" in response.data