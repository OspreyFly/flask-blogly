from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class Person(db.Model):
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    img_url = db.Column(db.String(200))

    # Define the relationship between Person and Post
    posts = db.relationship("Post", backref="author")

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    content = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Set the default value to the current timestamp

    # Define the foreign key relationship to Person
    author_id = db.Column(db.Integer, db.ForeignKey('people.id'))
