from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True, unique=False)
    audiofile = db.Column(db.String(64), index=True, unique=False)
    start = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Sample text:{} file:{} START:{} END:{}>'.format(self.text, self.audiofile, self.start, self.end)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    samples = db.relationship('Sample', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
