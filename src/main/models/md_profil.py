from main.app_init.database import db

class Profil (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Profil %r>' % self.description
