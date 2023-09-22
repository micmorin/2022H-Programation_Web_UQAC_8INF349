from main.models.md_post import Post
from main.models.md_reactions import Reaction
from main.app_init.database import db

# TOGGLE

def test_reaction_index_as_anonymous(client):
    with client.session_transaction():
        response = client.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(Reaction.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_reaction_index_as_lecteur(clientLecteur):
    with clientLecteur.session_transaction():
        reactions = Reaction.query.all()
        response = clientLecteur.get('/posts/'+str(Post.query.first().id), follow_redirects=True)
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        if string in response.get_data(as_text=True):
            clientLecteur.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)

        # Reaction 0
        response = clientLecteur.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        assert string in response.get_data(as_text=True)

        # Reaction 1
        response = clientLecteur.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[1].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[1].id)
        assert string in response.get_data(as_text=True)

        # Undo Reaction 0
        response = clientLecteur.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        assert string in response.get_data(as_text=True)

def test_reaction_index_as_auteur(clientAuteur):
    with clientAuteur.session_transaction():
        reactions = Reaction.query.all()
        response = clientAuteur.get('/posts/'+str(Post.query.first().id), follow_redirects=True)
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        if string in response.get_data(as_text=True):
            clientAuteur.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)

        # Reaction 0
        response = clientAuteur.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        assert string in response.get_data(as_text=True)

        # Reaction 1
        response = clientAuteur.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[1].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[1].id)
        assert string in response.get_data(as_text=True)

        # Undo Reaction 0
        response = clientAuteur.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        assert string in response.get_data(as_text=True)

def test_reaction_index_as_admin(clientAdmin):
     with clientAdmin.session_transaction():
        reactions = Reaction.query.all()
        response = clientAdmin.get('/posts/'+str(Post.query.first().id), follow_redirects=True)
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        if string in response.get_data(as_text=True):
            clientAdmin.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)

        # Reaction 0
        response = clientAdmin.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        assert string in response.get_data(as_text=True)

        # Reaction 1
        response = clientAdmin.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[1].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'active-react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[1].id)
        assert string in response.get_data(as_text=True)

        # Undo Reaction 0
        response = clientAdmin.get('/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id), follow_redirects=True)
        assert response.status_code == 200
        string = 'react" href="/posts/'+str(Post.query.first().id)+'/reaction/'+ str(reactions[0].id)
        assert string in response.get_data(as_text=True)


# CREATE
def test_reaction_create_as_anonymous(client):
    response = client.post("/admin/reaction/create", follow_redirects=True, data={'description':'test', 'icon':"bi-youtube"})
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data
    
def test_reaction_create_as_lecteur(clientLecteur):
    with clientLecteur:
        response = clientLecteur.post("/admin/reaction/create", follow_redirects=True, data={'description':'test', 'icon':"bi-youtube"})
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_reaction_create_as_auteur(clientAuteur):
    with clientAuteur:
        response = clientAuteur.post("/admin/reaction/create", follow_redirects=True, data={'description':'test', 'icon':"bi-youtube"})
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_reaction_create_as_admin(clientAdmin):
     with clientAdmin.session_transaction():
        response = clientAdmin.post("/admin/reaction/create", follow_redirects=True, data={'description':'test', 'icon':"bi-youtube"})
        assert response.status_code == 200
        assert b"Reaction enregistre" in response.data
        db.session.delete(Reaction.query.filter(Reaction.description=='test').first())
        db.session.commit()
    
# UPDATE

def test_reaction_update_as_anonymous(client):
    with client.session_transaction() as session:
        response = client.post("/admin/reaction/"+ str(Reaction.query.first().id)+"/edit", follow_redirects=True, data={'description':'test', 'icon':"bi-youtube"})
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_reaction_update_as_lecteur(clientLecteur):
    with clientLecteur.session_transaction() as session:
        response = clientLecteur.post("/admin/reaction/"+ str(Reaction.query.first().id)+"/edit", follow_redirects=True, data={'description':'test', 'icon':"bi-youtube"})
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_reaction_update_as_auteur(clientAuteur):
    with clientAuteur.session_transaction() as session:
        response = clientAuteur.post("/admin/reaction/"+ str(Reaction.query.first().id)+"/edit", follow_redirects=True, data={'description':'test', 'icon':"bi-youtube"})
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_reaction_update_as_admin(clientAdmin):
     with clientAdmin.session_transaction() as session:
        request = Reaction.query.first()
        copy = [request.description,request.icone]
        response = clientAdmin.post("/admin/reaction/"+ str(Reaction.query.first().id)+"/edit", follow_redirects=True, data={'description':'test', 'icon':"bi-youtube"})
        assert response.status_code == 200
        assert b"La reaction a ete mis a jour" in response.data

        p = Reaction.query.first()
        p.description = copy[0]
        p.icone = copy[1]
        db.session.commit()


# DESTROY

def test_reaction_destroy_as_anonymous(client):
    with client.session_transaction() as session:
        response = client.post("/admin/reaction/"+ str(Reaction.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Please log in to access this page" in response.data
    
def test_reaction_destroy_as_lecteur(clientLecteur):
    with clientLecteur.session_transaction() as session:
        response = clientLecteur.post("/admin/reaction/"+ str(Reaction.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data

def test_reaction_destroy_as_auteur(clientAuteur):
    with clientAuteur.session_transaction() as session:
        response = clientAuteur.post("/admin/reaction/"+ str(Reaction.query.first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Home Page" in response.data
    
def test_reaction_destroy_as_admin(clientAdmin):
     with clientAdmin.session_transaction() as session:
        db.session.add(Reaction(description='test', icone="bi-youtube"))
        db.session.commit()
        response = clientAdmin.post("/admin/reaction/"+ str(Reaction.query.filter(Reaction.description=='test').first().id), follow_redirects=True)
        assert response.status_code == 200
        assert b"La reaction a ete supprime!" in response.data