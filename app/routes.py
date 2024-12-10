from urllib.parse import urlsplit
from flask_login import login_required, login_user, current_user, logout_user
from app import app, db
import sqlalchemy as sa
from app.models import User, Expense
from app.forms import UserRegisterForm, UserLoginForm, AddExpenseForm
from flask import redirect, render_template, flash, request, url_for


# index
@app.route('/')
def index():
    return render_template('base.html')


@app.route('/dashboard')
@login_required
def dashboard():
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
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

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
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # TODO: Show user profile ifno and edit profile link


@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    form = AddExpenseForm()
    if form.validate_on_submit():
        # build the expense object
        expense = Expense(
            title=form.title.data,
            amount=form.amount.data,
            expense_date=form.date.data,
            description=form.description.data,
            creator=current_user
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added succesfully')
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html', form=form)
