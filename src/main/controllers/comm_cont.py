from flask_login import current_user, login_required
from main.models.md_comments import Comment
from flask import render_template, request, redirect, url_for, flash
from main.app_init.database import db
from datetime import datetime

@login_required
def create(post_id):
    if request.method == 'POST':
        body = request.values.get('body')
        if body is None or body =='':
            flash('Commentaire vide!')
        else:
            new_comm = Comment(body=body, 
                            pub_date = datetime.date(datetime.utcnow()),
                            post_id=post_id, user=current_user)
            db.session.add(new_comm)
            db.session.commit()
            flash('Commentaire enregistre!')
    return redirect(url_for('posts.show',post_id=post_id))

@login_required
def update(post_id): 
    if request.method == 'POST':
        comm = Comment.query.get_or_404(request.form['commID'])
        if comm.user_id == current_user.id or current_user.profil.description == "admin":
            comm.body = request.form['body']
            comm.rev_date = datetime.date(datetime.utcnow())
            db.session.commit()
            flash("Le commentaire a ete mis a jour") 
        else:
            flash("Mission impossible")
        return redirect(url_for('posts.show',post_id=post_id))

@login_required
def destroy(post_id):
    if request.method == 'POST':
        comm = Comment.query.get_or_404(request.form['commID'])
        if comm.user_id == current_user.id or current_user.profil.description == "admin":
            db.session.delete(comm)
            db.session.commit()
            flash('Le commentaire a ete supprime!')
        else:
            flash("Mission impossible")
        return redirect(url_for('posts.show',post_id=post_id))
