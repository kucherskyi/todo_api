#!venv/bin/python

from flask import Flask, render_template
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config.from_object('config')
db = SQLAlchemy(app)

from mod import controllers
db.create_all()
