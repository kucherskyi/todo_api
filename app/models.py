#!env/bin/python

from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))
    info = db.Column(db.String(100))
    email = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.String, server_default=db.func.now())
    updated_at = db.Column(db.String, server_default=db.func.now())

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def admin(self):
        return self.is_admin


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True)
    description = db.Column(db.String(100))
    status = db.Column(db.String(10))
    created_at = db.Column(db.String, server_default=db.func.now())
    updated_at = db.Column(db.String, server_default=db.func.now())