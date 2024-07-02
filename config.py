import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    RECAPTCHA_SECRET_KEY = '6LckD6EfAAAAAEHzq9XhuBlj_tutx-PlA-KNDa3Q'
    RECAPTCHA_PUBLIC_KEY = '6LckD6EfAAAAAKqk5lcYli_Get0k-ZzNQxADIA4q'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/rpg_gym_app'
