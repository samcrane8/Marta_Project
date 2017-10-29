from flask import Flask
from flask import request

from flaskapp import app

from API import API

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
