from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from comic_inventory.forms import ComicForm
from comic_inventory.models import Comic, db
from comic_inventory.helpers import random_quote_generator

site = Blueprint('site', __name__, template_folder = 'site_templates')


@site.route('/')
def home():
    print('look at this cool project. Would you just look at it')
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    comicform = ComicForm()

    try:
        if request.method == 'POST' and comicform.validate_on_submit():
            name = comicform.name.data
            description = comicform.description.data
            price = comicform.price.data 
            quality = comicform.quality.data
            if comicform.random_quote.data:
                random_quote = comicform.random_quote.data 
            else:
                random_quote = random_quote_generator()
            user_token = current_user.token

            comic = Comic(name, description, price, quality, random_quote, user_token)

            db.session.add(comic)
            db.session.commit()

            return redirect(url_for('site.profile'))
    
    except:
        raise Exception('Comic not created, check your info and try again!')

    user_token = current_user.token
    comics = Comic.query.filter_by(user_token = user_token)


    return render_template('profile.html', form = comicform, comics = comics)