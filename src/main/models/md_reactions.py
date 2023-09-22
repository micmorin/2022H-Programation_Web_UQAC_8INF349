from main.app_init.database import db

class article_reactions(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    reaction_id = db.Column(db.Integer, db.ForeignKey('reaction.id'), nullable=False)

    post = db.relationship('Post')
    user = db.relationship('User')
    reaction = db.relationship('Reaction')
    
    def __repr__(self):
        return '<Reaction %r>' % self.reaction_id

class Reaction (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)
    icone = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Reaction %r>' % self.description
