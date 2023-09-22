from main.models.md_profil import Profil
from main.app_init.database import db

# INDEX

def test_adminEtProfil_index_as_anonymous(client):
    response = client.get("/admin/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    
def test_adminEtProfil_index_as_lecteur(clientLecteur):
    with clientLecteur:
        response = clientLecteur.get("/admin/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_adminEtProfil_index_as_auteur(clientAuteur):
    with clientAuteur:
        response = clientAuteur.get("/admin/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_adminEtProfil_index_as_admin(clientAdmin):
     with clientAdmin:
        response = clientAdmin.get("/admin/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Gestion Administrateur" in response.data

# CREATE
def test_adminEtProfil_create_as_anonymous(client):
    response = client.post("/admin/profil/create", follow_redirects=True, data={'description':'test'})
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    
def test_adminEtProfil_create_as_lecteur(clientLecteur):
    with clientLecteur:
        response = clientLecteur.post("/admin/profil/create", follow_redirects=True, data={'description':'test'})
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_adminEtProfil_create_as_auteur(clientAuteur):
    with clientAuteur:
        response = clientAuteur.post("/admin/profil/create", follow_redirects=True, data={'description':'test'})
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_adminEtProfil_create_as_admin(clientAdmin):
     with clientAdmin.session_transaction():
        response = clientAdmin.post("/admin/profil/create", follow_redirects=True, data={'description':'test'})
        assert response.status_code == 200
        assert b"Profil enregistre" in response.data
        db.session.delete(Profil.query.filter(Profil.description=='test').first())
        db.session.commit()
    
# UPDATE

def test_adminEtProfil_update_as_anonymous(client):
    with client.session_transaction() as session:
        response = client.post("/admin/profil/"+ str(Profil.query.first().id)+"/edit", follow_redirects=True, data={'description':'test'})
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_adminEtProfil_update_as_lecteur(clientLecteur):
    with clientLecteur.session_transaction() as session:
        response = clientLecteur.post("/admin/profil/"+ str(Profil.query.first().id)+"/edit", follow_redirects=True, data={'description':'test'})
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_adminEtProfil_update_as_auteur(clientAuteur):
    with clientAuteur.session_transaction() as session:
        response = clientAuteur.post("/admin/profil/"+ str(Profil.query.first().id)+"/edit", follow_redirects=True, data={'description':'test'})
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_adminEtProfil_update_as_admin(clientAdmin):
     with clientAdmin.session_transaction() as session:
        request = Profil.query.first()
        copy = request.description
        response = clientAdmin.post("/admin/profil/"+ str(request.id)+"/edit", follow_redirects=True, data={'description':'test'})
        assert response.status_code == 200
        assert b"Le profil a ete mis a jour" in response.data

        p = Profil.query.first()
        p.description = 'admin'
        db.session.commit()


# DESTROY

def test_adminEtProfil_destroy_as_anonymous(client):
    with client.session_transaction() as session:
        response = client.post("/admin/profil/"+ str(Profil.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_adminEtProfil_destroy_as_lecteur(clientLecteur):
    with clientLecteur.session_transaction() as session:
        response = clientLecteur.post("/admin/profil/"+ str(Profil.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_adminEtProfil_destroy_as_auteur(clientAuteur):
    with clientAuteur.session_transaction() as session:
        response = clientAuteur.post("/admin/profil/"+ str(Profil.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data
    
def test_adminEtProfil_destroy_as_admin(clientAdmin):
    # Used Profile
     with clientAdmin.session_transaction() as session:
        response = clientAdmin.post("/admin/profil/"+ str(Profil.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Le profil est utilise par un utilisateur!" in response.data

    # New Profile
        db.session.add(Profil(description='test'))
        db.session.commit()
        response = clientAdmin.post("/admin/profil/"+ str(Profil.query.filter(Profil.description=='test').first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Le profil a ete supprime!" in response.data