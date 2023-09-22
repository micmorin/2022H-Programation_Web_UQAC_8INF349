from main.app_init.database import db
from main.models.md_user import User
from main.models.md_balise import Balise, article_balises
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.Date, nullable=False)
    rev_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title

    def to_json(self):
        author = User.query.get_or_404(self.user_id)
        balises = article_balises.query.filter_by(post=self).all()
        balises_array = []
        for b in balises:
            balises_array.append(b.balise.to_json())
        return {"id":self.id,
                "title":self.title,
                "body":self.body,
                "pub_date":self.pub_date,
                "rev_date":self.rev_date,
                "status":self.status,
                "author":author.to_json(), 
                "balises":balises_array}
