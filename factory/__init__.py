import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://efzxgcjjwtasbe:0eda20e400c55ab4a96ce12acdf5c884ae7bebefb4d96afc709dbf5fa365b561@ec2-54-160-202-3.compute-1.amazonaws.com:5432/d980j4rblo8327'
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