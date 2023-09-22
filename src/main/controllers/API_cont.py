import json
from queue import Empty
from flask import Blueprint, jsonify, request, redirect, url_for
from main.models.md_post import Post
from main.models.md_balise import Balise, article_balises
from main.app_init.database import db
from flask_login import current_user, login_required
from datetime import datetime

def all_posts():
    posts = Post.query.all()
    if posts is Empty:
        return jsonify({"message":"no articles found"}), 404
    else:
        posts_obj = []
        for p in posts:
            posts_obj.append(p.to_json())
        return jsonify({"message":"ok", "data": posts_obj}), 200

def one_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({"message":"ok", 'data':post.to_json()}), 200

@login_required
def create_post():
    if current_user.profil.description != "lecteur":
        record = json.loads(request.data)

        # POST
        post = Post(
            title = record['Title'], 
            body = record['Body'],
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = record['Published'],
            user = record['Auteur']
        )
        db.session.add(post)
        db.session.commit()

        # balises en string vers balises en array
        balises = []
        tempString = ""
        for tempChar in record['Balises']:
            if tempChar == ' ' or tempChar == ',':
                if tempString != '':
                    balises.append(tempString)
                    tempString = ""
            else:
                tempString += tempChar

        if (tempChar != ' ' or tempChar != ',') and tempString != "":
            balises.append(tempString)

        # creer or fetch la balise puis ajoute la paire post-balise
        for balise in balises:
            queryBalise = Balise.query.filter_by(description=balise).all()
            if queryBalise == []:
                bal = Balise(description=balise)
                db.session.add(bal)
                db.session.commit()
                db.session.add(article_balises(post_id=post.id,balise_id=bal.id))
                db.session.commit()
            else:
                bal = Balise.query.get_or_404(queryBalise[0].id)
                db.session.add(article_balises(post_id=post.id,balise_id=bal.id))
                db.session.commit()

        return jsonify({"message":"post created", 
                        "id":post.id}),201  
    else:
        return jsonify({"message":"user can not create a post"}),403

@login_required
def update_post():
    record = json.loads(request.data)
    post = Post.query.get_or_404(record['id'])
    if post.user_id == current_user.id or current_user.profil.description == "admin":   
        
        #POST
        post.title = record['Title'], 
        post.body = record['Body'],
        post.rev_date = datetime.date(datetime.utcnow()),
        post.status = record['Published'],
        post.user = record['Auteur']
        db.session.commit()

        # detruire les liens post-balise
        balises = article_balises.query.filter_by(post_id=post.id).all()
        for b in balises:
            db.session.delete(b)
        db.session.commit()

    # Creer les nouveaux liens post-balises
        
         # balises en string vers balises en array
        bs = []
        tempString = ""
        for tempChar in record['Balises']:
            if tempChar == ' ' or tempChar == ',':
                if tempString != '':
                    balises.append(tempString)
                    tempString = ""
            else:
                tempString += tempChar

        if (tempChar != ' ' or tempChar != ',') and tempString != "":
            bs.append(tempString)

        for balise in bs:
            queryBalise = Balise.query.filter_by(description=balise).first()
            if queryBalise is None:
                bal = Balise(description=balise)
                db.session.add(bal)
                db.session.commit()
                db.session.add(article_balises(post_id=post.id,balise_id=bal.id))
                db.session.commit()
            else:
                db.session.add(article_balises(post_id=post.id,balise_id=queryBalise.id))
                db.session.commit()

        return jsonify({"message":"post updated",
                        "id":post.id}),204
    else:
        return jsonify({"message":"user can not update this post"}),403

@login_required
def destroy_post(id):
    record = json.loads(request.data)
    post = Post.query.get_or_404(record['id'])
    if post.user_id == current_user.id or current_user.profil.description == "admin":  

        #POST  
        db.session.delete(post)
        db.session.commit()

        #BALISE-POST
        bs = article_balises.query.filter_by(post_id=post.id).all()
        for b in bs:
            db.session.delete(b)
        db.session.commit()

        return jsonify({"message":"post deleted"}),204
    else:
        return jsonify({"message":"user can not delete this post"}),403