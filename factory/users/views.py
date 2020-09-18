# users/views.py
from factory import app, request_source
from flask import render_template, Blueprint, redirect, url_for, request, abort, jsonify, make_response
from factory import db
from factory.models import Users, Token
import uuid
import jwt
from functools import wraps
from werkzeug.security import check_password_hash
import datetime
from flask_cors import cross_origin
import socket

users = Blueprint('users', __name__)

# Login admin
@users.route('/api/v1/admin', methods=['POST', 'GET'])
def login():

	if request.method == 'POST':

		if f"{request_source}admin" in request.headers.get("Referer"):

			data =  request.get_json(silent=True)

			if not data or not data.get('username') or not data.get('password'):
				return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

			user = Users.query.filter_by(username=str(data.get('username'))).first()

			if user is not None:

				if check_password_hash(user.password, str(data.get('password'))):
					token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

					token_id = token.decode('UTF-8')

					hostname = socket.gethostname()
					ip_address = socket.gethostbyname(hostname)

					token_add = Token(str(token_id), int(user.id), 1, ip_address, hostname)

					db.session.add(token_add)
					db.session.commit()

					return jsonify({
						'token': token_id,
						'id': user.id,
						'username': user.username,
						'public_id': user.public_id
						})
				else:
					error = 'wrongpass'
					return jsonify({
						'error': error
						})
			else:
				error = 'wronguser'
				return jsonify({
						'error': error
						})

		else:
			abort(403)
	else:
			abort(403)


# Insert new admin
@users.route('/api/v1/insert_admin', methods=['POST', 'GET'])
def insert():

	if request.method == 'POST':

		if f"{request_source}dashboard" in request.headers.get("Referer"):

			data =  request.get_json(silent=True)

			username = data.get('username')
			password = data.get('password')

			new_user = Users(username=username, password=password)

			db.session.add(new_user)
			db.session.commit()

			return jsonify({'success': 'done'})

		else:
			abort(403)
	else:
			abort(403)


@users.route('/api/v1/get_token_data', methods=['POST', 'GET'])
def get_token_data():

	if request.method == 'POST':
		if f"{request_source}" in request.headers.get("Referer"):

			data = request.get_json(silent=True)
			request_token = data.get('token')

			check_token = Token.query.filter_by(token=request_token).first()

			if check_token is not None:

				hostname = socket.gethostname()
				ip_address = socket.gethostbyname(hostname)

				token = check_token.token
				token_valid = check_token.valid
				token_ip = check_token.ip_address
				token_hostname = check_token.host_name


				if token_valid == 1 and hostname == token_hostname and token_ip == ip_address:

					return jsonify({
						'authenticated': True,
						'token': token,
						'id': check_token.token_owner.id,
						'username': check_token.token_owner.username,
						'public_id': check_token.token_owner.public_id
						})

				else:
					return jsonify({
						'authenticated': False
					})
			else:
				return jsonify({
					'authenticated': False
				})
		else:
			abort(403)
	else:
		abort(403)