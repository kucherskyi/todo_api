#!venv/bin/python

from app import db
from flask.ext.sqlalchemy import SQLAlchemy


class Base(db.Model):
    
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())
    

class User(Base):
    __tablename__ = 'users'
    name = db.Column(db.String(32))
    password_hash = db.Column(db.String(64))
    info = db.Column(db.String(100))
    email = db.Column(db.String(100))
    is_admin = db.Column(db.SmallInteger)
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)




class Task(Base):
    __tablename__ = 'tasks'
    title = db.Column(db.String(32))
    description = db.Column(db.String(100))
    status = db.Column(db.String(10))
    att = db.relationship('Attachment', backref="post", cascade="all, delete-orphan" , lazy='dynamic')


class Attachment(Base):
    __tablename__ = 'attachments'
    owner = db.Column(db.String(100))
    file_url = db.Column(db.String(10))
    task_id = db.Column(db.Integer, db.ForeignKey('Task.id'))

    
