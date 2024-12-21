import sqlalchemy as sa
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm

from app import db
from app.forms import AddExpenseForm, EditExpenseForm
from app.models.expense import Expense
from app.utils.db_utils import get_user_expense_or_404

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
        return redirect(url_for('expenses.expenses'))
    return render_template('add_expense.html', form=form)


@expense_bp.route('/expenses')
@login_required
def expenses():
    '''Shows total list of expense filtered by request arguments'''

    # Add search by title feature to the expenses
    search_query = request.args.get('search', default='')

    query = (
        sa.select(Expense)
        .where(Expense.creator == current_user)
        .order_by(Expense.expense_date))

    if search_query:
        query = query.where(
            Expense.title.ilike(f"%{search_query}%".lower())
        )

    total_amount = db.session.execute(
        sa.select(sa.func.sum(Expense.amount))
        .where(Expense.creator == current_user)
        .where(
            Expense.title.ilike(f"%{search_query}%") if search_query else True)
    ).scalar() or 0  # Default to 0 if no results

    page = request.args.get('page', default=1)
    page = int(page)
    print(type(page))
    per_page = 10
    expenses_pagination = db.paginate(
        select=query, page=page, per_page=per_page)

    return render_template(
        'expenses.html', expenses_pagination=expenses_pagination,
        search_query=search_query, total_amount=total_amount)


@expense_bp.route("/expense/<expense_id>")
@login_required
def show_expense(expense_id):
    """Show the expense"""
    expense = get_user_expense_or_404(expense_id)
    form = FlaskForm()
    return render_template('expense.html', expense=expense, form=form)


@expense_bp.route('/expense/edit/<expense_id>', methods=['POST', 'GET'])
@login_required
def edit_expense(expense_id):
    # Build the form
    form = EditExpenseForm()
    expense = get_user_expense_or_404(expense_id)
    if form.validate_on_submit():
        expense.expense_date = form.date.data
        expense.title = form.title.data
        expense.amount = form.amount.data
        expense.description = form.description.data
        db.session.commit()
        flash("Expense updated!")
        return redirect(url_for('expenses.show_expense',
                                expense_id=expense_id))
    return render_template('edit_expense.html', form=form, expense=expense)


@expense_bp.route("/expense/delete/<expense_id>", methods=['POST', 'GET'])
@login_required
def delete_expense(expense_id):
    '''Deletes the expense'''
    expense = get_user_expense_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense Deleted Successfully')
    return redirect(url_for('expenses.expenses'))
