import logging, os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import wtforms_json


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

wtforms_json.init()

# Logging settings
if os.environ.get('HEROKU') is None:
    handler = RotatingFileHandler(
        'testshop.log', maxBytes=1 * 1024 * 1024, backupCount=1
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
else:
    handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.info('testshop startup')

from app import views, models
