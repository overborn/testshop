import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import wtforms_json


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
wtforms_json.init()

handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

from app import views, models
