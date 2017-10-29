from flask import Flask
from flask import request

#from authentication import UserAuthentication
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy

app = Flask('SarOS Back-End')

# app = Flask(__name__)
CORS(app)