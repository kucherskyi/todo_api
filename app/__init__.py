#!venv/bin/python

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config.from_object('config')
db = SQLAlchemy(app)

from mod import controllers
db.create_all()
