import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'akinator-mini.sqlite')
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources=r'/api/*', headers='Content-Type', support_credentials=True)

db = SQLAlchemy(app)

Migrate(app, db)

# Global
request_source = 'http://createinc.000webhostapp.com/'
backend_source = 'https://akinator-mini.herokuapp.com/'

# Blueprints
from factory.users.views import users
from factory.game.views import game

app.register_blueprint(users)
app.register_blueprint(game)