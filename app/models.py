from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(80), index=True,
                                             unique=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128),
                                                     nullable=False)

    def set_password(self, password):
        '''Hashes the password and stores it'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''Verifies the password against the stored hash.'''
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
