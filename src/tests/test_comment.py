from main.models.md_comments import Comment
from main.models.md_post import Post
from main.models.md_user import User
from main.app_init.database import db
from flask import url_for
from datetime import datetime

# CREATE
def test_comment_create_as_anonymous(client,app):
    with app.app_context(), app.test_request_context():
        response = client.post(url_for('comments.create',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_comment_create_as_lecteur(clientLecteur,app):
   with app.app_context(), app.test_request_context():
        response = clientLecteur.post(url_for('comments.create',post_id=Post.query.first().id),data={'body':'test'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Commentaire enregistre!" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test').first())
        db.session.commit()

        response = clientLecteur.post(url_for('comments.create',post_id=Post.query.first().id),data={'body':''}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Commentaire vide!" in response.data

def test_comment_create_as_auteur(clientAuteur,app):
    with app.app_context(), app.test_request_context():
        response = clientAuteur.post(url_for('comments.create',post_id=Post.query.first().id),data={'body':'test'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Commentaire enregistre!" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test').first())
        db.session.commit()

        response = clientAuteur.post(url_for('comments.create',post_id=Post.query.first().id),data={'body':''}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Commentaire vide!" in response.data

def test_comment_create_as_admin(clientAdmin,app):
     with app.app_context(), app.test_request_context():
        response = clientAdmin.post(url_for('comments.create',post_id=Post.query.first().id),data={'body':'test'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Commentaire enregistre!" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test').first())
        db.session.commit()

        response = clientAdmin.post(url_for('comments.create',post_id=Post.query.first().id),data={'body':''}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Commentaire vide!" in response.data
    
# UPDATE

def test_comment_update_as_anonymous(client,app):
    with app.app_context(), app.test_request_context():
        response = client.post(url_for('comments.update',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_comment_update_as_lecteur(clientLecteur,app):
    with app.app_context(), app.test_request_context():
        # Update Self
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="lecteur").first()))
        db.session.commit()
        response = clientLecteur.post(url_for('comments.update',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Le commentaire a ete mis a jour" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test2').first())
        db.session.commit()

        #Update Other
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="admin").first()))
        db.session.commit()
        response = clientLecteur.post(url_for('comments.update',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Mission impossible" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test').first())
        db.session.commit()

def test_comment_update_as_auteur(clientAuteur,app):
     with app.app_context(), app.test_request_context():
        # Update Self
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="auteur").first()))
        db.session.commit()
        response = clientAuteur.post(url_for('comments.update',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Le commentaire a ete mis a jour" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test2').first())
        db.session.commit()

        #Update Other
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="admin").first()))
        db.session.commit()
        response = clientAuteur.post(url_for('comments.update',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Mission impossible" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test').first())
        db.session.commit()

def test_comment_update_as_admin(clientAdmin,app):
    with app.app_context(), app.test_request_context():
        # Update Other
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="lecteur").first()))
        db.session.commit()
        response = clientAdmin.post(url_for('comments.update',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Le commentaire a ete mis a jour" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test2').first())
        db.session.commit()

        #Update Self
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="admin").first()))
        db.session.commit()
        response = clientAdmin.post(url_for('comments.update',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Le commentaire a ete mis a jour" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test2').first())
        db.session.commit()

# DESTROY

def test_comment_destroy_as_anonymous(client,app):
    with app.app_context(), app.test_request_context():
        response = client.post(url_for('comments.destroy',post_id=Post.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_comment_destroy_as_lecteur(clientLecteur,app):
    with app.app_context(), app.test_request_context():
        # Destroy Self
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="lecteur").first()))
        db.session.commit()
        response = clientLecteur.post(url_for('comments.destroy',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Le commentaire a ete supprime!" in response.data

        #Destroy Other
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="admin").first()))
        db.session.commit()
        response = clientLecteur.post(url_for('comments.destroy',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Mission impossible" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test').first())
        db.session.commit()

def test_comment_destroy_as_auteur(clientAuteur,app):
    with app.app_context(), app.test_request_context():
        # Destroy Self
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="auteur").first()))
        db.session.commit()
        response = clientAuteur.post(url_for('comments.destroy',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Le commentaire a ete supprime!" in response.data

        #Destroy Other
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="admin").first()))
        db.session.commit()
        response = clientAuteur.post(url_for('comments.destroy',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Mission impossible" in response.data

        db.session.delete(Comment.query.filter(Comment.body=='test').first())
        db.session.commit()
    
def test_comment_destroy_as_admin(clientAdmin,app):
    with app.app_context(), app.test_request_context():
        # Destroy Other
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="lecteur").first()))
        db.session.commit()
        response = clientAdmin.post(url_for('comments.destroy',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Le commentaire a ete supprime!" in response.data

        #Destroy Self
        db.session.add(Comment(body='test', pub_date = datetime.date(datetime.utcnow()),
                            post_id=Post.query.first().id, 
                            user=User.query.filter(User.username=="admin").first()))
        db.session.commit()
        response = clientAdmin.post(url_for('comments.destroy',post_id=Post.query.first().id),
            data={'commID':Comment.query.filter(Comment.body=='test').first().id,'body':'test2'}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Le commentaire a ete supprime!" in response.data