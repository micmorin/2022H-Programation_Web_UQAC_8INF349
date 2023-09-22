# coding=utf-8
try:
    from main.app import create_app
    from main.app_init.database import db
    from main.models.md_user import User
    from main.models.md_post import Post
    from main.models.md_comments import Comment
    from main.models.md_profil import Profil
    from main.models.md_reactions import Reaction, article_reactions
    from main.models.md_balise import Balise, article_balises
    from datetime import datetime
    from werkzeug.security import generate_password_hash


    app = create_app()
    db.create_all(app = create_app())
    with app.app_context():
        db.session.delete(Profil.query.filter_by(description='test').first())
        db.session.commit()

        p = Profil.query.first()
        p.description = 'admin'
        db.session.commit()

        guest = User(
            name="lecteur_nom",username='lecteur', email='lecteur@example.com', 
            password=generate_password_hash("lecteur"))
        db.session.add(guest)
        db.session.commit()
except Exception as e:
    print(e, type(e))
    input()