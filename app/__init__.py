from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import wtforms_json

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
wtforms_json.init()

from app import views, models
