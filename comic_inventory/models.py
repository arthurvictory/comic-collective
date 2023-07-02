from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


# Adding flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import secret module
import secrets

# Import for LoginManager and UserMixing
#help us login our users and store their credentials
from flask_login import UserMixin, LoginManager

# import Flask-Marshmallow
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    comic = db.relationship('Comic', backref = 'owner', lazy = True)

    def __init__(self, email, username, password, first_name = '', last_name = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username

    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"User {self.email} has been added to the database. WOOOOOOO!"
    
class Comic(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision = 10, scale = 2))
    quality = db.Column(db.String(150), nullable = True)
    random_quote = db.Column(db.String, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, quality, random_quote, user_token):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.quality = quality
        self.random_quote = random_quote
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Comic book, {self.name} has been added to the database! WOOO!"
    
class ComicSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'quality', 'random_quote']

comic_schema = ComicSchema()
comics_schema = ComicSchema(many = True)