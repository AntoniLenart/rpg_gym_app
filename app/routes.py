from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import ExerciseData, Workout, UserExercise
from app.forms import WorkoutForm

import config

bp = Blueprint('routes', __name__)

CONFIG = config.Config()


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@bp.route('/exercises', methods=['GET'])
def exercises():
    return render_template('exercises.html', exercise_data=ExerciseData.query.all())

@bp.route('/workouts', methods=['GET'])
@login_required
def workouts():
    return render_template('workouts.html', workouts_data=current_user.workouts)

@bp.route('/workouts/add_workout', methods=['GET', 'POST'])
@login_required
def add_workout():
    workout = Workout(user=current_user)
    form = WorkoutForm()
    if request.method == 'POST':
        exercise_data = ExerciseData.query.get(form.exercise.data)
        user_exercise = UserExercise(
            name=form.exercise.data,
            muscle_part=exercise_data.muscle_part,
            xp_reward=exercise_data.xp_reward,
            sets=form.sets.data,
            reps=form.reps.data,
            workout=workout
            )
    return render_template('add_workout.html', form=form)