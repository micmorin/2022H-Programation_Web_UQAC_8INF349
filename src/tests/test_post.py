from main.models.md_balise import article_balises, Balise
from main.models.md_user import User
from main.models.md_post import Post
from main.app_init.database import db
from flask import url_for
from datetime import datetime

# INDEX

def test_post_index_as_anonymous(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('posts.index'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data
    
def test_post_index_as_lecteur(app, clientLecteur):
    with app.app_context(), app.test_request_context():
        response = clientLecteur.get(url_for('posts.index'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data

def test_post_index_as_auteur(app, clientAuteur):
    with app.app_context(), app.test_request_context():
        response = clientAuteur.get(url_for('posts.index'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data

def test_post_index_as_admin(app, clientAdmin):
    with app.app_context(), app.test_request_context():
        response = clientAdmin.get(url_for('posts.index'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data

# CREATE
def test_post_create_as_anonymous(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('posts.create'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_post_create_as_lecteur(app, clientLecteur):
    with app.app_context(), app.test_request_context():
        response = clientLecteur.get(url_for('posts.create'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data

def test_post_create_as_auteur(app, clientAuteur):
    with app.app_context(), app.test_request_context():
        response = clientAuteur.get(url_for('posts.create'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Ajouter un Article" in response.data

def test_post_create_as_admin(app, clientAdmin):
      with app.app_context(), app.test_request_context():
        response = clientAdmin.get(url_for('posts.create'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Ajouter un Article" in response.data

# STORE

def test_post_store_as_anonymous(app, client):
    with app.app_context(), app.test_request_context():
        #Save
        response = client.post(url_for('posts.store',status=0), follow_redirects=True, 
            data={'title':'test_title', 'body':'test_body', 'tags':'test_tag'})
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data

        #Publish
        response = client.post(url_for('posts.store',status=1), follow_redirects=True, 
            data={'title':'test_title', 'body':'test_body', 'tags':'test_tag'})
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
         
def test_post_store_as_lecteur(app, clientLecteur):
    with app.app_context(), app.test_request_context():
        #Save
        response = clientLecteur.post(url_for('posts.store',status=0), follow_redirects=True, 
            data={'title':'test_title', 'body':'test_body', 'tags':'test_tag'})
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data
        assert b"Article enregistre!" not in response.data

        #Publish
        response = clientLecteur.post(url_for('posts.store',status=1), follow_redirects=True, 
            data={'title':'test_title', 'body':'test_body', 'tags':'test_tag'})
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data
        assert b"Article enregistre!" not in response.data

def test_post_store_as_auteur(app, clientAuteur):
    with app.app_context(), app.test_request_context():
        #Save
        response = clientAuteur.post(url_for('posts.store',status=0), follow_redirects=True, 
            data={'title':'test_title', 'body':'test_body', 'tags':'test_tag'})
        assert response.status_code == 200
        assert b"Article enregistre!" in response.data
        db.session.delete(Post.query.filter_by(title='test_title').first())
        db.session.commit()

        #Publish
        response = clientAuteur.post(url_for('posts.store',status=1), follow_redirects=True, 
            data={'title':'test_title', 'body':'test_body', 'tags':'test_tag'})
        assert response.status_code == 200
        assert b"Article publie!" in response.data
        db.session.delete(article_balises.query.filter(
            article_balises.balise==Balise.query.filter(Balise.description=='test_tag').first(),
            article_balises.post==Post.query.filter(Post.title=='test_title').first()).first())
        db.session.delete(Balise.query.filter(Balise.description=='test_tag').first())    
        db.session.delete(Post.query.filter(Post.title=='test_title').first())
        db.session.commit()

def test_post_store_as_admin(app, clientAdmin):
    with app.app_context(), app.test_request_context():
        #Save
        response = clientAdmin.post(url_for('posts.store',status=0), follow_redirects=True, 
            data={'title':'test_title', 'body':'test_body'})
        assert response.status_code == 200
        assert b"Article enregistre!" in response.data
        db.session.delete(Post.query.filter_by(title='test_title').first())
        db.session.commit()

        #Publish
        response = clientAdmin.post(url_for('posts.store',status=1), follow_redirects=True, 
            data={'title':'test_title', 'body':'test_body', 'tags':'test_tag'})
        assert response.status_code == 200
        assert b"Article publie!" in response.data
        db.session.delete(article_balises.query.filter(
            article_balises.balise==Balise.query.filter(Balise.description=='test_tag').first(),
            article_balises.post==Post.query.filter(Post.title=='test_title').first()).first())
        db.session.delete(Balise.query.filter(Balise.description=='test_tag').first())    
        db.session.delete(Post.query.filter(Post.title=='test_title').first())
        db.session.commit()
    
# Show

def test_post_show_as_anonymous(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('posts.show',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Post Show" in response.data
    
def test_post_show_as_lecteur(app, clientLecteur):
   with app.app_context(), app.test_request_context():
        response = clientLecteur.get(url_for('posts.show',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Post Show" in response.data

def test_post_show_as_auteur(app, clientAuteur):
    with app.app_context(), app.test_request_context():
        response = clientAuteur.get(url_for('posts.show',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Post Show" in response.data

def test_post_show_as_admin(app, clientAdmin):
     with app.app_context(), app.test_request_context():
        response = clientAdmin.get(url_for('posts.show',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Post Show" in response.data

# UPDATE

def test_post_update_as_anonymous(app, client):
    with app.app_context(), app.test_request_context():
        new_post = Post(
            title ='test_title', 
            body = 'test_body',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = User.query.first())
        db.session.add(new_post)
        db.session.commit()
        response = client.post(url_for('posts.update',post_id=new_post.id), follow_redirects=True, 
            data={'title':'test_title2', 'body':'test_body2'})
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
            
        db.session.delete(new_post)
        db.session.commit()
    
def test_post_update_as_lecteur(app, clientLecteur):
    with app.app_context(), app.test_request_context():
        new_post = Post(
            title ='test_title', 
            body = 'test_body',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = User.query.first())
        db.session.add(new_post)
        db.session.commit()
        response = clientLecteur.post(url_for('posts.update',post_id=new_post.id), follow_redirects=True, 
            data={'title':'test_title2', 'body':'test_body2'})
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data
            
        db.session.delete(new_post)
        db.session.commit()

def test_post_update_as_auteur(app, clientAuteur):
   with app.app_context(), app.test_request_context():
        new_post = Post(
            title ='test_title', 
            body = 'test_body',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = User.query.filter(User.username=='auteur').first())
        db.session.add(new_post)
        db.session.commit()
        response = clientAuteur.post(url_for('posts.update',post_id=new_post.id), follow_redirects=True, 
            data={'title':'test_title2', 'body':'test_body2'})
        assert response.status_code == 200
        assert b"a ete mis a jour" in response.data
            
        db.session.delete(new_post)
        db.session.commit()

def test_post_update_as_admin(app, clientAdmin):
     with app.app_context(), app.test_request_context():
        new_post = Post(
            title ='test_title', 
            body = 'test_body',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = User.query.filter(User.username=='admin').first())
        db.session.add(new_post)
        db.session.commit()
        response = clientAdmin.post(url_for('posts.update',post_id=new_post.id), follow_redirects=True, 
            data={'title':'test_title2', 'body':'test_body2'})
        assert response.status_code == 200
        assert b"a ete mis a jour" in response.data
            
        db.session.delete(new_post)
        db.session.commit()

# DESTROY

def test_post_destroy_as_anonymous(app, client):
    with app.app_context(), app.test_request_context():
        new_post = Post(
            title ='test_title', 
            body = 'test_body',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = User.query.filter(User.username=='auteur').first())
        db.session.add(new_post)
        db.session.commit()
        response = client.post(url_for('posts.destroy',post_id=new_post.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
            
        db.session.delete(new_post)
        db.session.commit()
    
def test_post_destroy_as_lecteur(app, clientLecteur):
    with app.app_context(), app.test_request_context():
        new_post = Post(
            title ='test_title', 
            body = 'test_body',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = User.query.filter(User.username=='auteur').first())
        db.session.add(new_post)
        db.session.commit()
        response = clientLecteur.post(url_for('posts.destroy',post_id=new_post.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Articles de SpotiNyk" in response.data
            
        db.session.delete(new_post)
        db.session.commit()

def test_post_destroy_as_auteur(app, clientAuteur):
    with app.app_context(), app.test_request_context():
        new_post = Post(
            title ='test_title', 
            body = 'test_body',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = User.query.filter(User.username=='auteur').first())
        db.session.add(new_post)
        db.session.commit()
        response = clientAuteur.post(url_for('posts.destroy',post_id=new_post.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"a ete supprime" in response.data

def test_post_destroy_as_admin(app, clientAdmin):
    with app.app_context(), app.test_request_context():
        new_post = Post(
            title ='test_title', 
            body = 'test_body',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = User.query.filter(User.username=='admin').first())
        db.session.add(new_post)
        db.session.commit()
        response = clientAdmin.post(url_for('posts.destroy',post_id=new_post.id), follow_redirects=True)
        assert response.status_code == 200
        assert b"a ete supprime" in response.data