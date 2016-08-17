import logging, os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import wtforms_json


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

wtforms_json.init()

# Logging settings
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.info('testshop startup')

from app import views, models
