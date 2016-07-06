DEBUG = True
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_COMMIT_ON_TEARDOWN= True
SQLALCHEMY_TRACK_MODIFICATIONS = False
