from factory import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dateutil.tz import tzlocal
import uuid
from time import gmtime, strftime


# Users Table
class Users(db.Model):

	__tablename__  = 'users'

	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.Text, nullable=False, default=int(uuid.uuid4()))
	username = db.Column(db.String(64), unique=True, index=True)
	password = db.Column(db.Text)
	tokener = db.relationship('Token', backref='token_owner', lazy=True)


	def __init__(self, username, password):

		self.username = username
		self.password = generate_password_hash(password)

class Token(db.Model):

	__tablename__ = 'tokens'

	id = db.Column(db.Integer, primary_key=True)
	user = db.relationship(Users)
	token = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	valid = db.Column(db.Integer, nullable=False, default=1)
	ip_address = db.Column(db.Text)
	host_name = db.Column(db.Text)
	time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __init__(self, token, user_id, valid, ip_address, host_name):

		self.token = token
		self.user_id = user_id
		self.valid = valid
		self.ip_address = ip_address
		self.host_name = host_name

# Questions table
class Questions(db.Model):

	__tablename__ = 'questions'

	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.Text)
	notice = db.Column(db.Text)

	def __init__(self, question, notice):
		self.question = question
		self.notice = notice

# Questions table
class Guess(db.Model):

	__tablename__ = 'guess'

	id = db.Column(db.Integer, primary_key=True)
	guess = db.Column(db.String(128))
	questions = db.Column(db.String(128))
	picture = db.Column(db.Text)

	def __init(self, guess, questions, picture):
		self.guess = guess
		self.questions = questions
		self.picture = picture

# Sessions table
class Sessions(db.Model):

	__tablename__ = 'sessions'

	id = db.Column(db.Integer, primary_key=True)
	questions = db.Column(db.Text)
	answers = db.Column(db.Text)
	guess = db.Column(db.String(128))
	found = db.Column(db.Integer, nullable=False, default=0)
	accepted = db.Column(db.Integer, nullable=False, default=0)
	time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __init__(self, questions, answers, guess, found, accepted):

		self.questions = questions
		self.answers = answers
		self.guess = guess
		self.found = found
		self.accepted = accepted