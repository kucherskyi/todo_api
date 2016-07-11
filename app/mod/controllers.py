#!venv/bin/python

from flask import request, render_template,flash, g, session, redirect, url_for, abort, jsonify
from app import app, db
import datetime
import os
from models import User, Task, Attachment
from flask.ext.sqlalchemy import SQLAlchemy


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
    email = request.json.get('email')
    if User.query.filter_by(name=name).first() is not None:
        abort(400)
    user = User(name=name, info=info, is_admin=is_admin, email=email, password_hash = password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'name': user.name}), 201)


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'name': user.name})


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
        al.append({'Task': row.title})
    return jsonify(al)


@app.route('/api/tasks', methods=['POST'])
def new_task():
    title = request.json.get('title')
    description = request.json.get('description')
    status = request.json.get('status')
    created_at = str(datetime.datetime.now())
    updated_at = str(datetime.datetime.now())
    
    task = Task(title=title, description=description, status=status, att = att)
    db.session.add(task)
    db.session.commit()
    return (jsonify({'created': task.title}), 201)


@app.route('/api/tasks/<int:id>')

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


@app.route('/api/attachments')
def get_attachments():
    attachment = Attachment.query.all()
    al = []
    for row in attachment:
        al.append({'attachment': row.owner})
    return jsonify(al)


@app.route('/api/attachments', methods=['POST'])
def new_attachment():
    owner = request.json.get('owner')
    file_url = request.json.get('file_url')
    task_id = request.json.get('task_id')

    attachment = Attachment(owner=owner, file_url=file_url, status=status, task_id = task_id)
    db.session.add(attachment)
    db.session.commit()
    return (jsonify({'created': attachment.owner}), 201)


@app.route('/api/attachments/<int:id>')

def get_attachment(id):
    attachment = Attachment.query.get(id)
    if not attachment:
        abort(400)
    return jsonify({attachment.owner: attachment.file_url})


@app.route('/api/attachments/<int:id>', methods=['PUT'])
def update_attachment(id):
    attachment = Attachment.query.get(id)
    if not attachment:
        abort(400)
    attachment.owner = request.json.get('owner')
    attachment.updated_at = str(datetime.datetime.now())
    db.session.add(attachment)
    db.session.commit()
    return jsonify({attachment.owner: attachment.owner})


@app.route('/api/attachments/<int:id>', methods=['DELETE'])
def delete_attachment(id):
    attachment = Attachment.query.get(id)
    if not attachment:
        abort(400)
    db.session.delete(attachment)
    db.session.commit()
    return jsonify({'status': 'deleted'}, 200)
