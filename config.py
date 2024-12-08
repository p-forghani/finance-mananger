import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # TODO: Remove the default SECRET_KEY for production.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
