# project/tasks/views.py

# IMPORTS
from flask import render_template, Blueprint, request, redirect, url_for, flash, Markup
from flask_login import current_user, login_required
from project import db
from project.models import Tasks, User
from .forms import TasksForm, EditTasksForm



# CONFIG
tasks_blueprint = Blueprint('tasks', __name__, template_folder='templates')


# ROUTES
@tasks_blueprint.route('/all_tasks', methods=['GET', 'POST'])
@login_required
def all_tasks():
    """Render homepage"""
    all_user_tasks = Tasks.query.filter_by(user_id=current_user.id)
    return render_template('all_tasks.html', tasks=all_user_tasks)


@tasks_blueprint.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TasksForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_task = Tasks(form.task_name.data, form.description.data, form.finished.data, current_user.id)
                db.session.add(new_task)
                db.session.commit()
                message = Markup(
                    "<strong>Well done!</strong> Task added successfully!")
                flash(message, 'success')
                return redirect(url_for('home'))
            except:
                db.session.rollback()
                message = Markup(
                    "<strong>Oh snap!</strong>! Unable to add item.")
                flash(message, 'danger')
    return render_template('add_task.html', form=form)

@tasks_blueprint.route('/edit_task/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(tasks_id):
    form = EditTasksForm(request.form)
    item_with_task = db.session.query(Tasks, User).join(User).filter(Tasks.id == tasks_id).first()
    if item_with_task is not None:
        if current_user.is_authenticated and item_with_task.Items.user_id == current_user.id:
            if request.method == 'POST':
                if form.validate_on_submit():
                    try:
                        item = Tasks.query.get(tasks_id)
                        item.name = form.name.data
                        item.notes = form.notes.data
                        db.session.commit()
                        message = Markup("Item edited successfully!")
                        flash(message, 'success')
                        return redirect(url_for('home'))
                    except:
                        db.session.rollback()
                        message = Markup(
                            "<strong>Error!</strong> Unable to edit item.")
                        flash(message, 'danger')
            return render_template('edit_item.html', item=item_with_task, form=form)
        else:
            message = Markup(
                "<strong>Error!</strong> Incorrect permissions to access this item.")
            flash(message, 'danger')
    else:
        message = Markup("<strong>Error!</strong> Item does not exist.")
        flash(message, 'danger')
    return redirect(url_for('home'))
