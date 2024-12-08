from app import app, db
import sqlalchemy as sa
from app.models import User
from app.forms import UserRegisterForm
from flask import render_template, flash


# index
@app.route('/')
def index():
    user = {'first_name': 'pouria'}  # noqa
    return render_template('base.html')


# User registration
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You signed up successfully")
    return render_template('register.html', form=form)


# User sign in
@app.route('/login')
def login():
    pass


@app.route('/userlist')
def userlist():
    users = db.session.scalars(
        sa.select(User)
    ).all()
    return repr(users)
