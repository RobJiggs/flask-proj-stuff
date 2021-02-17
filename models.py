from datetime import datetime
from mentor import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user=User.query.filter(id==user_id).first()
    if user != '':
        return User.query.get(int(user_id))
    else:

        user = Usermentor.query.filter(id == user_id).first()
        return Usermentor.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    desiredfield= db.Column(db.String(60))
    job= db.Column(db.String(60))
    status= db.Column(db.String(20), nullable=False, default='Mentee')
    mentor = db.Column(db.Integer, db.ForeignKey('usermentor.id'))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Usermentor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    field = db.Column(db.String(60))
    job = db.Column(db.String(60))
    status = db.Column(db.String(20), nullable=False, default='Mentor')
    experience= (db.Integer)
    mentee = db.relationship('User', backref='link', lazy=True)

    def __repr__(self):
        return f"UserMentor('{self.username}','{self.status}','{self.experience}', '{self.email}','{self.mentee}, '{self.image_file}')"

class Jobfield(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='defaultfield.jpg')
    jtitles= db.relationship('Jobtitle', backref='Job', lazy=True)

    def __repr__(self):
        return f"Jobfield('{self.name}','{self.image_file}')"


class Jobtitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='defaultjob.jpg')
    jobfield_id= db.Column(db.Integer, db.ForeignKey('jobfield.id'), nullable=False)

    def __repr__(self):
        return f"Jobtitle('{self.name}', '{self.image_file}',)"

