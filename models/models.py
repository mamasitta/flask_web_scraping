from flask_sqlalchemy import SQLAlchemy
from db import db


class Task(db.Model):
    __tablename__ = 'Task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))
    result = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.String(50))

    def __repr__(self):
        return '<Task %r>' % self.title


class Page(db.Model):
    __tablename__ = 'Page'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    task_id = db.Column(db.Integer, db.ForeignKey('Task.id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('pages', lazy=True))

    def __repr__(self):
        return '<Page %r>' % self.name