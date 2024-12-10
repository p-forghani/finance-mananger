from datetime import datetime

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, EmailField, FloatField,
                     PasswordField, StringField, SubmitField, TextAreaField,
                     ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app import db
from app.models import User


class UserRegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), Length(1, 64)])
    last_name = StringField('Last Name', validators=[
        DataRequired(), Length(1, 64)
    ])
    email = EmailField('Email', validators=[
        DataRequired(), Length(max=64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat Password', validators=[
        DataRequired(), EqualTo('password')
    ])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        # Check if email does not exist on db
        user = db.session.scalar(
            sa.select(User).where(User.email == email.data)
        )
        if user is not None:
            raise ValidationError("You have signed up previously, login")

    def validate_password(self, password):
        # TODO: Ensure password contain enough characters and signs
        pass


class UserLoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(), Length(max=64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class AddExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    amount = FloatField('Amount', validators=[DataRequired()])
    description = TextAreaField("Description")
    date = DateField('Date', default=datetime.today())
