from main.app_init.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    profil_id = db.Column(db.Integer, db.ForeignKey('profil.id'), nullable=False, default=3)

    profil = db.relationship('Profil', backref='profils')

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)    

    def to_json(self):
        return {"id":self.id,
                "name":self.name,
                "email":self.email}