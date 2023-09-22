from main.app_init.database import db

class article_balises(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, primary_key=True)
    balise_id = db.Column(db.Integer, db.ForeignKey('balise.id'), nullable=False, primary_key=True)

    post = db.relationship('Post')
    balise = db.relationship('Balise')
    
    def __repr__(self):
        return '%r' % self.post_id

class Balise (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '%r' % self.id

    def to_json(self):
        return {"id":self.id,
                "description":self.description}
