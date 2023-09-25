from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)

"""Models for Blogly."""
class Person(db.Model):
    __tablename__ = "people"

    def __init__(self, first_name, last_name, img_url):
        self.first_name = first_name
        self.last_name = last_name
        self.img_url = img_url

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    img_url = db.Column(db.String(50))
    
