"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

DEFAULT_IMG_URL = 'https://image.flaticon.com/icons/png/128/1077/1077114.png'

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    @property
    def full_name(self):
        """Full name of user"""
        return f"{self.first_name} {self.last_name}"

