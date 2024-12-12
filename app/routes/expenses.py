from flask_login import login_required, current_user
from app.utils.db_utils import get_user_expense_or_404
from app import db
from app.models.expense import Expense
from app.forms import AddExpenseForm
from flask import redirect, render_template, flash, url_for
from flask import Blueprint

expense_bp = Blueprint('expenses', __name__)


@expense_bp.route('/expense', methods=['GET', 'POST'])
@login_required
def add_expense():
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
        return redirect(url_for('users.dashboard'))
    return render_template('add_expense.html', form=form)


@expense_bp.route("/expense/<expense_id>")
@login_required
def show_expense(expense_id):
    """Show the expense with the proper template"""
    expense = get_user_expense_or_404(expense_id)
    return render_template('expense.html', expense=expense)


@expense_bp.route('/expense/edit/expense_id')
@login_required
def edit_expense(expense_id):
    pass


@expense_bp.route("/expense/delete/<expense_id>", methods=['POST', 'GET'])
@login_required
def delete_expense(expense_id):
    '''Deletes the expense'''
    # TODO: delete an expense
    expense = get_user_expense_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense Deleted Successfully')
    return redirect(url_for('users.dashboard'))
