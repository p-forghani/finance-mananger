from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timezone
from flask_login import UserMixin
from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(80), index=True,
                                             unique=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128),
                                                     nullable=False)
    expenses: so.WriteOnlyMapped['Expense'] = so.relationship(
        back_populates='creator'
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


class Expense(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True,
                                             nullable=False)
    amount: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    expense_date: so.Mapped[date] = so.mapped_column(
        sa.Date, index=True, nullable=False
    )
    description: so.Mapped[str] = so.mapped_column(
        sa.String(256), default="", nullable=True
        )
    added_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    creator: so.Mapped[User] = so.relationship(back_populates='expenses')

    def __repr__(self) -> str:
        return (
            f"<Expense(title={self.title}, amount={self.amount}, "
            f"expense_date={self.expense_date}, added_at={self.added_at})>"
        )