from flask import abort
from app.models.expense import Expense
from flask_login import current_user


def get_user_expense_or_404(expense_id) -> Expense:
    """
    Fetch an expense by ID and ensure it belongs to the current user.
    If not, raise a 403 Forbidden error.
    """
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        abort(403)  # Forbidden
    return expense
