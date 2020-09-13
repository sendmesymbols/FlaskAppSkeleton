from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length


class TasksForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired(), Length(min=1, max=254)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=254)])
    finished = BooleanField('Finished ? ', default=False)


class EditTasksForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired(), Length(min=1, max=254)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=254)])
    finished = BooleanField('Finished ? ', default=False, render_kw={'checked': ''})
