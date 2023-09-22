from main.models.md_user import User
from main.app_init.database import db

# INDEX

def test_user_index_as_anonymous(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert b"Personnel" in response.data
    assert b"lecteur" not in response.data
    
def test_user_index_as_lecteur(clientLecteur):
    with clientLecteur:
        response = clientLecteur.get("/users/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Personnel" in response.data
        assert b"lecteur" in response.data

def test_user_index_as_auteur(clientAuteur):
    with clientAuteur:
        response = clientAuteur.get("/users/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Personnel" in response.data
        assert b"lecteur" not in response.data

def test_user_index_as_admin(clientAdmin):
     with clientAdmin:
        response = clientAdmin.get("/users/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Utilisateurs" in response.data

# CREATE
def test_user_create_as_anonymous(client):
    response = client.get("/users/create", follow_redirects=True)
    assert response.status_code == 200
    assert b"Enregistrement" in response.data
    
def test_user_create_as_lecteur(clientLecteur):
    with clientLecteur:
        response = clientLecteur.get("/users/create", follow_redirects=True)
        assert response.status_code == 200
        assert b"Enregistrement" in response.data

def test_user_create_as_auteur(clientAuteur):
    with clientAuteur:
        response = clientAuteur.get("/users/create", follow_redirects=True)
        assert response.status_code == 200
        assert b"Enregistrement" in response.data

def test_user_create_as_admin(clientAdmin):
     with clientAdmin:
        response = clientAdmin.get("/users/create", follow_redirects=True)
        assert response.status_code == 200
        assert b"Nouvel Utilisateur" in response.data

# STORE

def test_user_store_as_anonymous(app, client):
    with app.app_context():
        response = client.post("/users/store", follow_redirects=True, 
            data={'username':'test', 'password':'test', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        assert b"Utilisateur enregistre" in response.data
        assert b"test@email.com" in response.data
        db.session.delete(User.query.filter_by(username='test').first())
        db.session.commit()
         
def test_user_store_as_lecteur(app, clientLecteur):
    with clientLecteur.session_transaction():
        response = clientLecteur.post("/users/store", follow_redirects=True, 
            data={'username':'test', 'password':'test', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        assert b"Utilisateur enregistre" not in response.data
        assert b"test@email.com" not in response.data

def test_user_store_as_auteur(app, clientAuteur):
     with app.app_context():
        response = clientAuteur.post("/users/store", follow_redirects=True, 
            data={'username':'test', 'password':'test', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        assert b"Utilisateur enregistre" not in response.data
        assert b"test@email.com" not in response.data

def test_user_store_as_admin(app, clientAdmin):
    with app.app_context():
        response = clientAdmin.post("/users/store", follow_redirects=True, 
            data={'username':'test', 'password':'test', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        print(response.data)
        assert b'name="profil"' in response.data
        assert b"test@email.com" in response.data
        db.session.delete(User.query.filter_by(username='test').first())
        db.session.commit()
    
# UPDATE

def test_user_update_as_anonymous(client):
    with client.session_transaction() as session:
        user_test = User.query.first()
        response = client.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username':'test', 'password':'', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_user_update_as_lecteur(clientLecteur):
    with clientLecteur.session_transaction() as session:
        # Update Other
        user_test = User.query.filter(User.id != session['_user_id']).first()
        response = clientLecteur.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username':'test', 'password':'', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        assert b"mis a jour" not in response.data
        
        # Update Self
        user_test = User.query.filter(User.id == session['_user_id']).first()
        copy = [user_test.username, user_test.password, user_test.name, user_test.email]
        response = clientLecteur.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username':'test', 'password':'', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        assert b"mis a jour" in response.data

        # Undo Update Self
        response = clientLecteur.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username': copy[0], 'password':'', 'name':copy[2], 'email':copy[3]})

def test_user_update_as_auteur(clientAuteur):
    with clientAuteur.session_transaction() as session:
        # Update Other
        user_test = User.query.filter(User.id != session['_user_id']).first()
        response = clientAuteur.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username':'test', 'password':'', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        assert b"mis a jour" not in response.data
        
        # Update Self
        user_test = User.query.filter(User.id == session['_user_id']).first()
        copy = [user_test.username, user_test.password, user_test.name, user_test.email]
        response = clientAuteur.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username':'test', 'password':'', 'name':'test_nom', 'email':'test@email.com'})
        assert response.status_code == 200
        assert b"mis a jour" in response.data

        # Undo Update Self
        response = clientAuteur.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username': copy[0], 'password':'', 'name':copy[2], 'email':copy[3]})

def test_user_update_as_admin(clientAdmin):
     with clientAdmin.session_transaction() as session:
        # Update Other
        user_test = User.query.filter(User.id != session['_user_id']).first()
        copy = [user_test.username, user_test.password, user_test.name, user_test.email]
        response = clientAdmin.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username':'test', 'password':'', 'name':'test_nom', 'email':'test@email.com', 'profil':""})
        assert response.status_code == 200
        assert b"test_nom" in response.data

        # Undo Update Other
        response = clientAdmin.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username': copy[0], 'password':'', 'name':copy[2], 'email':copy[3], 'profil':""})
        
        # Update Self
        user_test = User.query.filter(User.id == session['_user_id']).first()
        copy = [user_test.username, user_test.password, user_test.name, user_test.email]
        response = clientAdmin.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username':'test', 'password':'', 'name':'test_nom', 'email':'test@email.com', 'profil':""})
        assert response.status_code == 200
        assert b"test_nom" in response.data

        # Undo Update Self
        response = clientAdmin.post("/users/"+ str(user_test.id) +"/edit", follow_redirects=True, 
                data={'username': copy[0], 'password':'', 'name':copy[2], 'email':copy[3], 'profil':""})

# DESTROY

def test_user_destroy_as_anonymous(client):
    with client.session_transaction() as session:
        user_test = User.query.first()
        response = client.post("/users/"+ str(user_test.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_user_destroy_as_lecteur(clientLecteur):
    with clientLecteur.session_transaction() as session:
        # Destroy Other
        user_test = User.query.filter(User.id != session['_user_id']).first()
        response = clientLecteur.post("/users/"+ str(user_test.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"supprime" not in response.data
        
        # Destroy Self
        user_test = User.query.filter(User.id == session['_user_id']).first()
        response = clientLecteur.post("/users/"+ str(user_test.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"supprime" not in response.data

def test_user_destroy_as_auteur(clientAuteur):
    with clientAuteur.session_transaction() as session:
        # Destroy Other
        user_test = User.query.filter(User.id != session['_user_id']).first()
        response = clientAuteur.post("/users/"+ str(user_test.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"supprime" not in response.data
        
        # Destroy Self
        user_test = User.query.filter(User.id == session['_user_id']).first()
        response = clientAuteur.post("/users/"+ str(user_test.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"supprime" not in response.data

def test_user_destroy_as_admin(clientAdmin):
     with clientAdmin.session_transaction() as session:
        # Destroy Other
        response = clientAdmin.post("/users/store", follow_redirects=True,
            data={'username':'test', 'password':'test', 'name':'test_nom', 'email':'test@email.com'})
        user_test = User.query.filter(User.username =='test').first()
        response = clientAdmin.post("/users/"+ str(user_test.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"supprime" in response.data

        # Destroy Self
        user_test = User.query.filter(User.id == session['_user_id']).first()
        response = clientAdmin.post("/users/"+ str(user_test.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"supprime" not in response.data
