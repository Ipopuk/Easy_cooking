from webapp.db import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=1)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    wishlist = db.Column(db.Text)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'User {self.id} - {self.username}'


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=1)
    title = db.Column(db.String, nullable=False)
    recipe = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text)
    image = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='cascade'),
        nullable=False
        )

    def __repr__(self):
        return f'Блюдо {self.title} - {self.ingredients}'
