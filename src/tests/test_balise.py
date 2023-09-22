from main.models.md_post import Post
from main.models.md_balise import Balise,article_balises
from main.app_init.database import db
from flask import url_for

# INDEX

def test_balise_index_as_anonymous(client):
    response = client.get("/balise/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Balises list" in response.data
    
def test_balise_index_as_lecteur(clientLecteur):
    with clientLecteur:
        response = clientLecteur.get("/balise/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Balises list" in response.data

def test_balise_index_as_auteur(clientAuteur):
    with clientAuteur:
        response = clientAuteur.get("/balise/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Balises list" in response.data

def test_balise_index_as_admin(clientAdmin):
     with clientAdmin:
        response = clientAdmin.get("/balise/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Balises list" in response.data

# CREATE

def test_balise_create_as_anonymous(client,app):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('balises.create',post_id=Post.query.first().id,string="test"), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_balise_create_as_lecteur(clientLecteur,app):
    with app.app_context(), app.test_request_context():
        response = clientLecteur.get(url_for('balises.create',post_id=Post.query.first().id,string="test"), follow_redirects=True)
        assert response.status_code == 200
        assert b"Balises list" in response.data

def test_balise_create_as_auteur(clientAuteur, app):
    with app.app_context(), app.test_request_context():
        response = clientAuteur.get(url_for('balises.create',post_id=Post.query.first().id,string="test"), follow_redirects=True)
        assert response.status_code == 200
        assert b"test" in response.data

        db.session.delete(article_balises.query.filter(article_balises.balise==Balise.query.filter(Balise.description=='test').first(),article_balises.post==Post.query.first()).first())
        db.session.delete(Balise.query.filter(Balise.description=="test").first())
        db.session.commit()

def test_balise_create_as_admin(clientAdmin,app):
    with app.app_context(), app.test_request_context():
        response = clientAdmin.get(url_for('balises.create',post_id=Post.query.first().id,string="test"), follow_redirects=True)
        assert response.status_code == 200
        assert b"test" in response.data

        db.session.delete(article_balises.query.filter(article_balises.balise==Balise.query.filter(Balise.description=='test').first(),article_balises.post==Post.query.first()).first())
        db.session.delete(Balise.query.filter(Balise.description=="test").first())
        db.session.commit()
    
# UPDATE

def test_balise_update_as_anonymous(client,app):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('balises.updateMany',post_id=Post.query.first().id,string="test test2"), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data

        response = client.post(url_for('balises.update',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data

def test_balise_update_as_lecteur(clientLecteur,app):
   with app.app_context(), app.test_request_context():
        response = clientLecteur.get(url_for('balises.updateMany',post_id=Post.query.first().id,string="test test2"), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

        response = clientLecteur.post(url_for('balises.update',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_balise_update_as_auteur(clientAuteur,app):
    with app.app_context(), app.test_request_context():
        response = clientAuteur.get(url_for('balises.updateMany',post_id=Post.query.first().id,string="test test2"), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data

        response = clientAuteur.get(url_for('balises.updateMany',post_id=Post.query.first().id,string='tourisme'), follow_redirects=True)

        response = clientAuteur.post(url_for('balises.update',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_balise_update_as_admin(clientAdmin,app):
     with app.app_context(), app.test_request_context():
        response = clientAdmin.get(url_for('balises.updateMany',post_id=Post.query.first().id,string="test test2"), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data

        response = clientAdmin.get(url_for('balises.updateMany',post_id=Post.query.first().id,string='tourisme'), follow_redirects=True)

        response = clientAdmin.post(url_for('balises.update',balise_id=Balise.query.first().id), data={'description':'test'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"mis a jour" in response.data

        response = clientAdmin.post(url_for('balises.update',balise_id=Balise.query.first().id), data={'description':'tourisme'}, follow_redirects=True)


# DESTROY

def test_balise_destroy_as_anonymous(client, app):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('balises.destroyMany',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data

        response = client.get(url_for('balises.updateMany',post_id=Post.query.first().id,string='tourisme'), follow_redirects=True)
    
        response = client.post(url_for('balises.destroy',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data

def test_balise_destroy_as_lecteur(clientLecteur, app):
    with app.app_context(), app.test_request_context():
        response = clientLecteur.get(url_for('balises.destroyMany',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

        response = clientLecteur.get(url_for('balises.updateMany',post_id=Post.query.first().id,string='tourisme'), follow_redirects=True)

        response = clientLecteur.post(url_for('balises.destroy',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_balise_destroy_as_auteur(clientAuteur, app):
    with app.app_context(), app.test_request_context():
        response = clientAuteur.get(url_for('balises.destroyMany',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data

        response = clientAuteur.get(url_for('balises.updateMany',post_id=Post.query.first().id,string='tourisme'), follow_redirects=True)
    
        db.session.add(Balise(description="test"))
        response = clientAuteur.post(url_for('balises.destroy',balise_id=Balise.query.filter(Balise.description == "test").first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_balise_destroy_as_admin(clientAdmin, app):
    with app.app_context(), app.test_request_context():
        response = clientAdmin.get(url_for('balises.destroyMany',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data

        response = clientAdmin.get(url_for('balises.updateMany',post_id=Post.query.first().id,string='tourisme'), follow_redirects=True)

        db.session.add(Balise(description="test"))
        response = clientAdmin.post(url_for('balises.destroy',balise_id=Balise.query.filter(Balise.description == "test").first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Balises list" in response.data

# SHOW

def test_balise_show_as_anonymous(client,app):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('balises.show',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Post Tag list" in response.data
    
def test_balise_show_as_lecteur(clientLecteur,app):
    with app.app_context(), app.test_request_context():
        response = clientLecteur.get(url_for('balises.show',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Post Tag list" in response.data

def test_balise_show_as_auteur(clientAuteur,app):
    with app.app_context(), app.test_request_context():
        response = clientAuteur.get(url_for('balises.show',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Post Tag list" in response.data

def test_balise_show_as_admin(clientAdmin,app):
    with app.app_context(), app.test_request_context():
        response = clientAdmin.get(url_for('balises.show',balise_id=Balise.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Post Tag list" in response.data