# coding=utf-8
try:
    from main.app import create_app
    from main.app_init.database import db
    from main.models.md_user import User
    from main.models.md_post import Post
    from main.models.md_comments import Comment
    from main.models.md_profil import Profil
    from main.models.md_reactions import Reaction, article_reactions
    from main.models.md_balise import Balise, article_balises
    from datetime import datetime
    from werkzeug.security import generate_password_hash


    app = create_app()
    print('Création de la base de données...')
    db.create_all(app = create_app())
    print('ok!\n')
    with app.app_context():
        print('Ajouter des profils...')
        prof1 = Profil(description="admin")
        prof2 = Profil(description="auteur")
        prof3 = Profil(description="lecteur")

        db.session.add(prof1)
        db.session.add(prof2)
        db.session.add(prof3)
        db.session.commit()

        print('Ajouter des utilisateurs...')
        admin = User(
            name="admin_nom", username='admin', email='admin@example.com', 
            password=generate_password_hash("admin"), profil=prof1)
        guest = User(
            name="lecteur_nom",username='lecteur', email='guest@example.com', 
            password=generate_password_hash("lecteur"))
        aut = User(
            name="auteur_nom",username='auteur', email='aut@example.com', 
            password=generate_password_hash("auteur"), profil=prof2)

        db.session.add(admin)
        db.session.add(guest)
        db.session.add(aut)
        db.session.commit()

        print('Ajout de publications...')
        
        p1 = Post(
            title ='Brick Tavern House', 
            body = "The Brick Tavern House is a former inn on the National Road west of St. Clairsville,Ohio, United States. One of the oldest National Road taverns still in existence, it was built in the early nineteenth century. Although it fell into dilapidation during the late twentieth century, it was named a historic site in 1995, and extensive restoration was to be performed in the early 2010s but to date, has not been. The tavern's construction date varies widely in different sources. A history of Belmont County published in 1903 proposed that it had been built in 1812;[2] the U.S. Department of Transportation believes that it was constructed in 1828;[3] a restoration firm, Centennial Preservation Group, states that it was erected in 1825;[4] and the National Park Service gives its construction year as 1831.[1] Built of brick on a foundation of sandstone, the tavern is covered with a tin roof and features elements of sandstone and slate.[5] The two-and-a-half-story building features a gabled roof, while the overall design includes a rear ell faced by porches on both sides.[3] Numerous taverns were constructed along the National Road in its earliest years, as the road saw its golden years between 1825 and 1845. However, the coming of railroads later in the century relegated the road to a farm track by 1900, and its businesses and towns were reduced to serving only local needs. Although it survived the neglect of long-distance travelers, the Brick Tavern House gradually fell into dilapidation; by 2012, its windows were boarded up, and the entire structure was tending toward collapse,[6] even though it was part of the campus of Ohio University East.[7] To save the building, the university applied for historic preservation grants from the federal government, and in September 2006 the U.S. Department of Transportation announced that they had been awarded $128,000 for restoration.[3] Restoration was forced to wait; early 2012 saw the tavern still deteriorating amid a protracted bidding process.[6] Ultimately, the Belmont County Commissioners agreed to permit bidding for renovation, including roof repairs, in April 2012,[8] and construction had been finished by June of the following year. Work was performed by Centennial Preservation Group,[4] with assistance by Hays Landscape Architecture.[9] In 1995, amid its deterioration, the Brick Tavern House was listed on the National Register of Historic Places, qualifying because of its place in local history; a secondary building was included with the tavern in the designation.[1] Part of its historical importance derives from its location next door to the Great Western Schoolhouse, another National Register-listed building; local school districts use the schoolhouse for field trips, and the restoration grant was awarded in hopes that the renovated tavern might become a museum in connection with the schoolhouse.[3] (c) wikipedia.org",
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = aut
        )

        p2 = Post(
            title ='East Langwell', 
            body = 'East Langwell is a small, remote crofting settlement in Rogart, Sutherland, Scottish Highlands and is in the Scottish council area of Highland.[1] West Langwell lies 2 miles directly northwest of East Langwell, and approximately 6 miles north of Golspie.',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = True,
            user = admin
        )

        p3 = Post(
            title ='Post3', 
            body = 'Body of Post 3',
            pub_date = datetime.date(datetime.utcnow()),
            rev_date = datetime.date(datetime.utcnow()),
            status = False,
            user = aut
        )

        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()

        print('Ajout de commentaires...')

        c1 = Comment(
            body = 'Interressant',
            pub_date = datetime.date(datetime.utcnow()),
            post = p1,
            user = guest
        )

        c2 = Comment(
            body = 'Ouais....',
            pub_date = datetime.date(datetime.utcnow()),
            post = p1,
            user = aut
        )

        c3 = Comment(
            body = 'Super!',
            pub_date = datetime.date(datetime.utcnow()),
            post = p2,
            user = admin
        )

        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()

        print('Ajout de reactions...')

        r1 = Reaction(description="Like",icone="bi-hand-thumbs-up-fill")
        r2 = Reaction(description="Applaud",icone="bi-award-fill")

        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()

        ar1 = article_reactions(post_id=p1.id,user_id=guest.id,reaction_id=r1.id)
        ar2 = article_reactions(post_id=p1.id,user_id=admin.id,reaction_id=r2.id)
        ar3= article_reactions(post_id=p1.id,user_id=aut.id,reaction_id=r1.id)
        ar4 = article_reactions(post_id=p2.id,user_id=admin.id,reaction_id=r2.id)

        db.session.add(ar1)
        db.session.add(ar2)
        db.session.add(ar3)
        db.session.add(ar4)
        db.session.commit()

        print('Ajout de balises...')

        t1 = Balise(description="tourisme")
        t2 = Balise(description="ville")

        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()

        tag1 = article_balises(post_id=p1.id,balise_id=t1.id)
        tag2 = article_balises(post_id=p2.id,balise_id=t2.id)
        tag3 = article_balises(post_id=p2.id,balise_id=t1.id)

        db.session.add(tag1)
        db.session.add(tag2)
        db.session.add(tag3)
        db.session.commit()

        print('ok, tout est prêt. Vous pouvez exécuter l\'application maintenant.')
        input()

except Exception as e:
    print(e, type(e))
    input()