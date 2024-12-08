from urllib.parse import urlsplit
from flask_login import login_user, current_user
from app import app, db
import sqlalchemy as sa
from app.models import User
from app.forms import UserRegisterForm, UserLoginForm
from flask import redirect, render_template, flash, request, url_for


# index
@app.route('/')
def index():
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


@app.route('/login', methods=['GET', 'POST'])
def login():

    # TODO: Change the dest url later
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = UserLoginForm()
    # Check user credentials
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )
        if (user is None) or (not user.check_password(form.password.data)):
            flash("Wrong email or password")
            return redirect(url_for('login'))
        # log the user in
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        # netloc is the network location (e.g., example.com, localhost:8000),
        # if netloc is not empty it means url contains domain
        # Full url including the domain name is ignored due to the security
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    return 'To be built'


# TODO: Delete this view for production
@app.route('/userlist')
def userlist():
    users = db.session.scalars(
        sa.select(User)
    ).all()
    return repr(users)
