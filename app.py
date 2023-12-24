"""Flask App for Flask Cafe."""

import os

from flask import Flask, render_template, flash, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, Cafe, db
from forms import CafeEditForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])

#     else:
#         g.user = None


# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes


@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )


@app.route('/cafes/add', methods=['GET', 'POST'])
def add_cafe():
    """Show form to add cafe and process it."""

    form = CafeEditForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_cafe = Cafe(**data)

        db.session.add(new_cafe)
        db.session.commit()

        flash(f'{new_cafe.name} added.')
        redirect_url = url_for('cafes/<int:cafe_id>', id=new_cafe.id)
        return redirect(redirect_url)

    render_template('add-form.html', form=form)


@app.route('/cafes/<int:cafe_id>/edit', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    """Show edit form for cafe and process it."""

    cafe = Cafe.query.get_or_404(cafe_id)
    form = CafeEditForm(obj=cafe)

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        cafe.name = data.name
        cafe.description = data.description
        cafe.url = data.url
        cafe.address = data.address
        cafe.city_code = data.city_code
        cafe.image_url = data.image_url

        db.session.commit()
        flash(f"{cafe.name} edited.")
        return redirect(f"/cafes/{cafe.id}")
       
    return render_template("edit-form.html", form=form)


