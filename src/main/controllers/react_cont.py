from queue import Empty
from flask_login import current_user, login_required
from main.models.md_reactions import Reaction, article_reactions
from flask import render_template, request, redirect, url_for, flash
from main.app_init.database import db
from datetime import datetime

@login_required
def toggle(post_id,react_id):
    reaction = article_reactions.query.get((post_id,current_user.get_id()))
    if reaction is None :
        rea = article_reactions(post_id=post_id, user_id=current_user.get_id(),reaction_id=react_id)
        db.session.add(rea)
        
    else:
        if reaction.reaction_id != react_id:
            reaction.reaction_id = react_id

        else:
            db.session.delete(reaction)

    db.session.commit()
    return redirect(url_for('posts.show',post_id=post_id))

@login_required
def create():
    if current_user.profil.description == "admin":
        p = Reaction(
            description=request.form['description']
            )
        if request.form['icon'] != "":
            p.icone=request.form['icon']
        db.session.add(p)
        db.session.commit()
        flash('Reaction enregistre!')
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('default.index'))

@login_required
def update(reaction_id):
    if current_user.profil.description == "admin":
        p = Reaction.query.get_or_404(reaction_id)
        if request.method == 'POST':
            p.description = request.form['description']
            if request.form['icon'] != "":
                p.icone=request.form['icon']
            db.session.commit()
            flash("La reaction a ete mis a jour!") 
        return redirect(url_for('admin.index')) 
    else:
        return redirect(url_for('default.index')) 

@login_required
def destroy(reaction_id):
    if current_user.profil.description == "admin":
        p = Reaction.query.get_or_404(reaction_id)
        db.session.delete(p)
        db.session.commit()
        flash("La reaction a ete supprime!")
        return redirect(url_for('admin.index'))   
    else:
        return redirect(url_for('default.index')) 