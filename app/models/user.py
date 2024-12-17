from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask import current_app, url_for
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from app.utils.auth import get_serializer

if TYPE_CHECKING:
    from app.models.expense import Expense  # Only for type hints


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(80), index=True,
                                             unique=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128),
                                                     nullable=False)
    expenses: so.WriteOnlyMapped['Expense'] = so.relationship(
        'Expense', back_populates='creator'
    )

    def set_password(self, password):
        '''Hashes the password and stores it'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''Verifies the password against the stored hash.'''
        return check_password_hash(self.password_hash, password)

    def get_reset_password_url(self):
        serializer = URLSafeTimedSerializer(
                current_app.config['SECRET_KEY'])
        token = serializer.dumps(self.id, salt='password-reset-salt')
        reset_url = url_for('users.reset_password', token=token,
                            _external=True)
        return reset_url

    def verify_token(token):
        try:
            serializer = get_serializer()
            # Attempt to load the token
            user_id = serializer.loads(token, max_age=3600,
                                       salt='password-reset-salt')
            # Returns the user info embedded in the token
            return user_id
        except SignatureExpired:
            # Token has expired
            return None
        except BadSignature:
            # Invalid token
            return None

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


@login .user_loader
def load_user(user_id):
    return db.session.get(User, user_id)
