from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.forms import UserLoginForm, UserRegisterForm
from app.models.user import User


users_bp = Blueprint('users', __name__)


# index
@users_bp.route('/')
def index():
    return render_template('base.html')


# User registration
@users_bp.route('/register', methods=['POST', 'GET'])
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


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('users.index')
        return redirect(next_page)

    form = UserLoginForm()
    # Check user credentials
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data)
        )
        if (user is None) or (not user.check_password(form.password.data)):
            flash("Wrong email or password")
            return redirect(url_for('users.login'))
        # log the user in
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        # netloc is the network location (e.g., example.com, localhost:8000),
        # if netloc is not empty it means url contains domain
        # Full url including the domain name is ignored due to the security
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('users.index')
        return redirect(next_page)

    return render_template('login.html', form=form)


@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.index'))


@users_bp.route('/profile')
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    # TODO: Show user profile info and edit profile link
