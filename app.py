#!venv/bin/python

import datetime
from flask import Flask, jsonify, abort, make_response, request, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
auth = HTTPBasicAuth()


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


@auth.verify_password
def verify_password(name, password):

    user = User.query.filter_by(name=name).first()
    if not user or not user.verify_password(password):
        return False
    return True


@app.route('/api/users')
def get_users():
    user = User.query.all()
    al = []
    for row in user:
        al.append({'User': row.name})
    return jsonify(al)


@app.route('/api/users', methods=['POST'])
def new_user():
    name = request.json.get('name')
    password = request.json.get('password')
    info = request.json.get('info')
    is_admin = request.json.get('is_admin')
    created_at = str(datetime.datetime.now())
    email = request.json.get('email')
    updated_at = str(datetime.datetime.now())
    if User.query.filter_by(name=name).first() is not None:
        abort(400)
    user = User(name=name, info=info, is_admin=is_admin, email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'name': user.name}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({user.is_admin: user.info})


@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    user.info = request.json.get('info')
    user.updated_at = str(datetime.datetime.now())
    db.session.add(user)
    db.session.commit()
    return jsonify({'name': user.info})


@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'deleted'}), 200


@app.route('/api/tasks')
def get_tasks():
    task = Task.query.all()
    al = []
    for row in task:
        al.append({'Task': row.name})
    return jsonify(al)


@app.route('/api/tasks', methods=['POST'])
def new_task():
    title = request.json.get('title')
    description = request.json.get('description')
    status = request.json.get('status')
    created_at = str(datetime.datetime.now())
    updated_at = str(datetime.datetime.now())
    task = Task(title=title, description=description, status=status)
    db.session.add(task)
    db.session.commit()
    return (jsonify({'created': task.title}), 201,
            {'Location': url_for('get_tasks', id=task.id, _external=True)})


@app.route('/api/tasks/<int:id>')
@auth.login_required
def get_task(id):
    task = Task.query.get(id)
    if not task:
        abort(400)
    return jsonify({task.title: task.status})


@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        abort(400)
    task.info = request.json.get('info')
    task.updated_at = str(datetime.datetime.now())
    db.session.add(task)
    db.session.commit()
    return jsonify({task.title: task.info})


@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        abort(400)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'status': 'deleted'}, 200)

if __name__ == '__main__':
    if not os.path.exists('test.db'):
        db.create_all()
        app.run(debug=True)
