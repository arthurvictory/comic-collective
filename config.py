import os

basedir = os.path.abspath(os.path.dirname(__file__))

 
class Config():
    """
        Set Config variables for the flask app.
        Using Envorinment variables where available
        create config variables if not done already.
    """
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess this, haha'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False