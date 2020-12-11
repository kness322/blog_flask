from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config


app = Flask(__name__)
app.config.from_object(config.DevelopementConfig)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для получения доступа'
login_manager.login_message_category = 'alert alert-danger'


from . import views
