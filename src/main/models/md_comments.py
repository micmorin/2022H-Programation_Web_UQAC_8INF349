from main.app_init.database import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.Date, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    post = db.relationship('Post', backref=db.backref('posts', lazy=True))
    user = db.relationship('User')

    def __repr__(self):
        return '<Post %r>' % self.body