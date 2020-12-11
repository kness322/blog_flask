from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    tablename__ = 'users',
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(500), nullable=True)
    create_on = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship('Profile', backref='user', uselist=False)
    articles = db.relationship('Article', backref='user')

    def __repr__(self):
        return f"<user {self.id}>"

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(db.Model, UserMixin):
    tablename__ = 'profiles',
    id = db.Column(db.Integer(), primary_key=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='defaultAvatar.png')
    firstname = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<profile {self.firstname} {self.lastname}>"

    def set_default_information(self):
        self.firstname, self.lastname = 'не указано', 'не указано'


class Article(db.Model, UserMixin):
    tablename__ = 'articles',
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=True)
    text = db.Column(db.String(500), nullable=True)
    create_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<article {self.title}>"
