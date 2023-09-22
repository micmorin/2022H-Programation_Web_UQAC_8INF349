from flask_login import current_user, login_required
from main.models.md_post import Post
from main.models.md_comments import Comment
from main.models.md_reactions import Reaction, article_reactions
from main.models.md_balise import Balise, article_balises
from flask import render_template, request, redirect, url_for, flash
from main.app_init.database import db
from datetime import datetime

def index():
    posts = Post.query.all()
    return render_template('post_list.html', posts=posts)

@login_required
def create():
    if current_user.profil.description != "lecteur":
        return render_template('post_create.html')
    else:
        return redirect(url_for('posts.index')) 

@login_required
def store(status):
    if current_user.profil.description != "lecteur":
        title = request.values.get('title')
        body = request.values.get('body')
        new_post = Post(title=title, body=body, 
                        pub_date = datetime.date(datetime.utcnow()),rev_date = datetime.date(datetime.utcnow()),
                        status=status, user=current_user)
        db.session.add(new_post)
        db.session.commit()
        if status:
            flash('Article publie!')
            if request.values.get('tags') is None:
                return redirect(url_for('posts.index'))
            else:
                return redirect(url_for('balises.create',post_id=new_post.id, string=request.values.get('tags')))
        else:
            flash('Article enregistre!')
            return redirect(url_for('posts.index'))  
    else:
        return redirect(url_for('posts.index'))  
            

def show(post_id):
    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post=post).order_by(Comment.pub_date.desc()).all()
    reactions = Reaction.query.all()
    rs = []
    for x in reactions:
        rs.append(
            {
                "id":x.id,
                "description":x.description,
                "icone":x.icone,
                "size":len(article_reactions.query.filter_by(post_id=post_id,reaction_id=x.id).all())
            }
        )
    balises=article_balises.query.filter_by(post_id=post_id).all()
    reaction = article_reactions.query.get((post_id,current_user.get_id()))
    print(post)
    return render_template('post_show.html', post = post, comments=comments, rs=rs, reaction=reaction, balises=balises)

@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id or current_user.profil.description == "admin": 
        if request.method == 'POST':
            post.title = request.form['title']
            post.body = request.form['body']
            post.rev_date = datetime.date(datetime.utcnow())
            db.session.commit()
            flash("L'article " + post.title + " a ete mis a jour") 
            if request.values.get('tags') is None:
                return redirect(url_for('posts.index'))
            else:
                return redirect(url_for('balises.updateMany',post_id=post.id, string=request.form['tags']))

        return render_template('post_update.html', post=post, balises=article_balises.query.filter_by(post_id=post_id).all()) 
    else:
        return redirect(url_for('posts.index'))

@login_required
def destroy(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id or current_user.profil.description == "admin": 
        db.session.delete(post)
        db.session.commit()
        flash("L'article a ete supprime!")
        if request.values.get('tags') is None:
            return redirect(url_for('posts.index'))
        else:
            return redirect(url_for('balises.destroyMany',post_id=post.id))
    else:
        return redirect(url_for('posts.index'))