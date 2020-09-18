from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/mini_akinator'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources=r'/api/*', headers='Content-Type', support_credentials=True)

db = SQLAlchemy(app)

Migrate(app, db)

# Global
request_source = 'http://createinc.000webhostapp.com/'
backend_source = 'http://127.0.0.1:5000/'

# Blueprints
from factory.users.views import users
from factory.game.views import game

app.register_blueprint(users)
app.register_blueprint(game)