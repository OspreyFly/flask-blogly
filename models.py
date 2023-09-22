from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)

"""Models for Blogly."""
class Person(db.Model):
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    img_url = db.Column(db.String(50))
    
#default="https://cdn.pixabay.com/photo/2017/06/13/12/53/profile-2398782_1280.png"