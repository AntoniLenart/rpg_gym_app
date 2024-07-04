from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import ExerciseData, Workout, UserExercise
from app.forms import WorkoutForm
from .app import db
from datetime import date

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
def add_workout(added_exercises=[]):
    form = WorkoutForm()
    if request.method == 'POST':
        if request.form['submit_button'] == 'add_exercise':
            exercise_data = ExerciseData.query.get(form.exercise.data)
            user_exercise = UserExercise(
                name=form.exercise.data,
                muscle_part=exercise_data.muscle_part,
                xp_reward=exercise_data.xp_reward,
                sets=form.sets.data,
                reps=form.reps.data,
                workout=None
                )
            added_exercises.append(user_exercise)
            return render_template('add_workout.html', form=form, added_exercises=added_exercises)

        elif request.form['submit_button'] == 'save_workout':
            current_workout = Workout(user=current_user, date=date.today(), xp=sum([ex.xp_reward * ex.sets for ex in added_exercises]))
            for ex in added_exercises:
                ex.workout = current_workout

            current_user.update_xp(current_workout.xp)

            db.session.add(current_workout)
            db.session.add_all(added_exercises)
            db.session.commit()

            added_exercises.clear()
            return render_template('workouts.html', workouts_data=current_user.workouts)
        
    added_exercises.clear()
    return render_template('add_workout.html', form=form)

@bp.route('/workouts/view_workout/<workout_id>')
@login_required
def view_workout(workout_id):
    exercises = Workout.query.get(workout_id).exercises
    return render_template('view_workout.html', exercises=exercises)