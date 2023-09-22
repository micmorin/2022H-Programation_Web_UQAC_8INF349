from main.models.md_profil import Profil
from main.models.md_reactions import Reaction
from main.models.md_user import User
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from main.app_init.database import db

@login_required
def index():
    if current_user.profil.description == "admin":
        profils = Profil.query.all()
        reactions = Reaction.query.all()
        return render_template('admin.html', profils=profils, reactions=reactions)
    else:
        return redirect(url_for('default.index'))

@login_required
def createProfil():
    if current_user.profil.description == "admin":
        p = Profil(
            description=request.form['description']
            )
        db.session.add(p)
        db.session.commit()
        flash('Profil enregistre!')
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('default.index'))

@login_required
def updateProfil(profil_id):
    if current_user.profil.description == "admin":
        p = Profil.query.get_or_404(profil_id)
        if request.method == 'POST':
            p.description = request.form['description']
            db.session.commit()
            flash("Le profil a ete mis a jour") 
        return redirect(url_for('admin.index')) 
    else:
        return redirect(url_for('default.index'))

@login_required
def destroyProfil(profil_id):
    if current_user.profil.description == "admin":
        p = Profil.query.get_or_404(profil_id)
        users = User.query.filter_by(profil_id=profil_id).all()
        if users == []:
            db.session.delete(p)
            db.session.commit()
            flash("Le profil a ete supprime!")
        else:
            flash("Le profil est utilise par un utilisateur!")
        return redirect(url_for('admin.index'))  
    else:
        return redirect(url_for('default.index')) 