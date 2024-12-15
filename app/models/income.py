from datetime import date, datetime, timezone

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db
from app.models.user import User


class Income(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    source: so.Mapped[str] = so.mapped_column(
        sa.String(128), index=True, nullable=False)
    amount: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    income_date: so.Mapped[date] = so.mapped_column(
        sa.Date, index=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(
        sa.String(256), default="", nullable=True)
    added_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(User.id), index=True)
    payee: so.Mapped[User] = so.relationship(back_populates='expenses')

    def __repr__(self) -> str:
        return (
            f"<Income(source={self.source}, amount={self.amount}, "
            f"income_date={self.income_date}, added_at={self.added_at})>"
        )
