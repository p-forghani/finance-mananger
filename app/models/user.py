from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import TYPE_CHECKING

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

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


@login .user_loader
def load_user(user_id):
    return db.session.get(User, user_id)
