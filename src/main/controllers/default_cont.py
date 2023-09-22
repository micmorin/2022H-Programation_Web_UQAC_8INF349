import flask
from main.models.md_post import Post
from main.models.md_user import User
from main.models.md_profil import Profil
from main.models.form_login import LoginForm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash

def index():
    posts = Post.query.all()
    users = User.query.all()
    profils = Profil.query.all()
    return render_template('index.html', posts=posts, users=users, profils=profils)

def login():
    form = LoginForm()
    if form.is_submitted():
        username = form.username.data
        passwd = form.password.data
        user = User.query.filter_by(username=username).first()
        next = flask.request.args.get('next')
        if user and check_password_hash(user.password, passwd):
            login_user(user)
            flash('Connexion reussie')
        else:
            flash('Identifiants invalides.')
            print("invalid login")

        return flask.redirect(next or flask.url_for('default.index')) 
        
    return render_template("login.html", form = form)

@login_required
def logout():
    logout_user()
    return redirect('/')

