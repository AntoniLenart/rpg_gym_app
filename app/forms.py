from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired
from app.models import ExerciseData


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class WorkoutForm(FlaskForm):
    exercise = SelectField('Exercise', validators=[DataRequired()])
    sets = IntegerField('Sets', validators=[DataRequired()])
    reps = IntegerField('Repetitions', validators=[DataRequired()])
    add_exercise = SubmitField('Add exercise')
    submit = SubmitField('Save workout')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exercises = ExerciseData.query.all()
        self.exercise.choices = [(ex.name, ex.name) for ex in exercises]
