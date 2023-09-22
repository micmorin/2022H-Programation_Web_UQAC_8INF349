from main.models.md_user import User
from main.models.md_profil import Profil
from main.models.form_register import RegisterForm
from flask import render_template, request, redirect, url_for, flash
from main.app_init.database import db
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, login_required

def index():
    users = User.query.all()
    profils = Profil.query.all()
    return render_template('user_list.html', users=users, profils=profils)

def create():
    return render_template('user_create.html', form=RegisterForm())

def store():
    if not current_user.is_authenticated or current_user.profil.description == 'admin':
        new_user = User(
            name=request.values.get('name'), 
            username=request.values.get('username'), 
            email=request.values.get('email'),
            password=generate_password_hash(request.values.get('password'))
            )
        db.session.add(new_user)
        db.session.commit()
        flash('Utilisateur enregistre!')
        if not current_user.is_authenticated:
            login_user(new_user)
    return redirect(url_for('default.index'))

@login_required
def update(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST' and (user_id == current_user.id or current_user.profil.description == "admin"):
        user.name = request.form['name']
        user.username = request.form['username']
        user.email = request.form['email']
        if request.form['password'] != "":
            user.password = generate_password_hash(request.form['password'])
        if current_user.profil.description == "admin" and request.form['profil'] != "":
            p = Profil.query.get_or_404(request.form['profil'])
            user.profil = p
        db.session.commit()
        flash("L'utilisateur " + user.username + " a ete mis a jour") 
    return redirect(url_for('users.index'))    

@login_required
def destroy(user_id):
    if current_user.profil.description == "admin" and user_id != current_user.id:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash("L'utilisateur a ete supprime!")
    return redirect(url_for('users.index'))
