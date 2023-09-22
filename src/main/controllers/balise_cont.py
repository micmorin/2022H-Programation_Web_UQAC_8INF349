from flask_login import login_required
from main.models.md_balise import Balise, article_balises
from main.models.md_post import Post
from main.app_init.database import db
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user

def index():
    balises = Balise.query.all()
    return render_template('balises_list.html', balises=balises)

@login_required
def create(post_id, string):
    if current_user.profil.description != "lecteur":
        # balises en string vers balises en array
        balises = []
        tempString = ""
        for tempChar in string:
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
                db.session.add(article_balises(post_id=post_id,balise_id=bal.id))
                db.session.commit()
            else:
                bal = Balise.query.get_or_404(queryBalise[0].id)
                db.session.add(article_balises(post_id=post_id,balise_id=bal.id))
                db.session.commit()
        return redirect(url_for('posts.show',post_id=post_id))
    else:
        return redirect(url_for('balises.index',post_id=post_id))


@login_required
def updateMany(post_id, string):
    if current_user.profil.description != "lecteur":
    # detruire les liens post-balise
        balises = article_balises.query.filter_by(post_id=post_id).all()
        for b in balises:
            db.session.delete(b)
        db.session.commit()

    # Creer les nouveaux liens post-balises
        
         # balises en string vers balises en array
        bs = []
        tempString = ""
        for tempChar in string:
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
                db.session.add(article_balises(post_id=post_id,balise_id=bal.id))
                db.session.commit()
            else:
                db.session.add(article_balises(post_id=post_id,balise_id=queryBalise.id))
                db.session.commit()

        return redirect(url_for('posts.index'))
    return redirect(url_for('default.index'))

def show(balise_id):
    posts = article_balises.query.filter_by(balise_id=balise_id).all()
    po = ""
    if posts == []:
        po = Balise.query.get_or_404(balise_id)

    return render_template('post_list_tag.html', posts=posts, po=po)

@login_required
def update(balise_id):
    if current_user.profil.description == "admin":
        b = Balise.query.get_or_404(balise_id)
        b.description = request.form['description']
        db.session.commit()
        flash("La balise a ete mis a jour") 
        return redirect(url_for('balises.index')) 
    else:
        return redirect(url_for('default.index'))

@login_required
def destroy(balise_id):
    if current_user.profil.description == "admin":
        bs = article_balises.query.filter_by(balise_id=balise_id).all()
        for b in bs:
            db.session.delete(b)
        
        b = Balise.query.get_or_404(balise_id)
        db.session.delete(b)

        db.session.commit()

        return redirect(url_for('balises.index'))
    else:
        return redirect(url_for('default.index'))

@login_required
def destroyMany(post_id):
    if current_user.profil.description != "lecteur":
        bs = article_balises.query.filter_by(post_id=post_id).all()
        for b in bs:
            db.session.delete(b)

        db.session.commit()
        return redirect(url_for('posts.index'))
    else:
        return redirect(url_for('default.index'))