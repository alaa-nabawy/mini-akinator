# game/views.py
from factory import app, request_source, backend_source
from flask import render_template, Blueprint, redirect, url_for, request, abort, jsonify, make_response
from factory import db
from factory.models import Users, Questions, Guess, Sessions
import uuid
import jwt
from functools import wraps
from werkzeug.security import check_password_hash
import datetime
from flask_cors import cross_origin
import socket
from factory.function.functions import *

game = Blueprint('game', __name__)

# Start Game
@game.route('/api/v1/start_game', methods=['POST', 'GET'])
def start_game():

	if request.method == 'POST':

		if f"{request_source}answer" in request.headers.get("Referer"):

			question = Questions.query.first()

			if question is not None:

				return jsonify({
					'id': question.id,
					'question': question.question,
					'notice': question.notice
					})
			else:
				return jsonify({
					'error': 'norecords'
					})
		else:
			abort(403)

	else:
			abort(403)


# Start Game
@game.route('/api/v1/guess', methods=['POST', 'GET'])
def guess():

	if request.method == 'POST':

		if f"{request_source}answer" in request.headers.get("Referer"):

			data = request.get_json(silent=True)

			data_question = []
			exclude = []
			all_qustions = []
			answers_list = []

			for question in data:

				answers_list.append(question.get('answer'))
				all_qustions.append(question.get('question_id'))

				if question.get('answer') == '1':

					data_question.append(question.get('question_id'))

				else:

					exclude.append(question.get('question_id'))

			guesses = Guess.query

			guessess_list = []

			for guess in guesses:

				list_of_question = get_list(guess.questions)

				if len(exclude) > 0:

					if similarity_score(list_of_question, exclude) == 0:

						if len(data_question) == 0:

							random_question = get_rand_question(list_of_question, data_question)

							get_new_question = Questions.query.get(int(random_question))

							return jsonify({
								'id': get_new_question.id,
								'question': get_new_question.question,
								'notice': get_new_question.notice
								})

						if similarity_score(list_of_question, data_question) > 0:

							if check_containing(list_of_question, data_question) == True:

								if similarity_score(list_of_question, data_question) < 0.8:

									random_question = get_rand_question(list_of_question, data_question)

									get_new_question = Questions.query.get(int(random_question))

									# Another question from the same guess to be sure of guess
									return jsonify({
									'id': get_new_question.id,
									'question': get_new_question.question,
									'notice': get_new_question.notice
									})

								# We got a guess
								return jsonify({
								'id': guess.id,
								'guess_name': guess.guess,
								'image': backend_source+'factory/static/guess_pic/' +guess.picture,
								'questions': all_qustions,
								'answers': answers_list
								})

				else:

					if similarity_score(list_of_question, data_question) > 0:

						if check_containing(list_of_question, data_question) == True:

							if similarity_score(list_of_question, data_question) < 0.8:

								random_question = get_rand_question(list_of_question, data_question)

								get_new_question = Questions.query.get(int(random_question))

								return jsonify({
								'id': get_new_question.id,
								'question': get_new_question.question,
								'notice': get_new_question.notice
								})
									
							return jsonify({
								'id': guess.id,
								'guess_name': guess.guess,
								'image': backend_source+'factory/static/guess_pic/' +guess.picture,
								'questions': all_qustions,
								'answers': answers_list
								})

			new_session = Sessions(questions=str(all_qustions), answers=str(answers_list), guess=0, found=0, accepted=0)
			db.session.add(new_session)
			db.session.commit()

			return jsonify({
				'message': 'noguess'
				})

		else:
			abort(403)

	else:
			abort(403)



# Start Game
@game.route('/api/v1/set_guess_image', methods=['POST', 'GET'])
def set_guess_image():

	if request.method == 'POST':

		if f"{request_source}dashboard" in request.headers.get("Referer"):

			img = request.files['guess_image']

			pic = add_pic(img, 'guess_pic', 400, 400)

			return jsonify({
				'filepath': backend_source+'static/guess_pic/' + pic,
				'image_name': pic
				})

		else:
			abort(403)

	else:
			abort(403)

# Start Game
@game.route('/api/v1/insert_guess', methods=['POST', 'GET'])
def insert_guess():

	if request.method == 'POST':

		if f"{request_source}dashboard" in request.headers.get("Referer"):

			data = request.get_json(silent=True)

			guess_name = data.get('name')
			pic = data.get('pic')
			questions = data.get('questions')

			questions_ids = []
			
			for question in questions:

				split_text = question.split('&')

				question_text = split_text[0]
				question_notice = split_text[1]


				# Check for a question with the same name
				check_question = Questions.query.filter_by(question=question_text).first()

				if check_question is not None:

					questions_ids.append(str(check_question.id))

				else:
					new_question = Questions(question=question_text, notice=question_notice)

					db.session.add(new_question)
					db.session.commit()

					get_new_question_id = Questions.query.filter_by(question=question_text).first()

					questions_ids.append(str(get_new_question_id.id))

			insert_guess = Guess(guess=guess_name, questions=str(questions_ids), picture=pic)

			db.session.add(insert_guess)
			db.session.commit()

			return jsonify({
				'message': 'done'
				})

		else:
			abort(403)

	else:
			abort(403)

# Start Game
@game.route('/api/v1/get_sessions', methods=['POST', 'GET'])
def get_sessions():

	if request.method == 'POST':


		sessions = Sessions.query

		sessions_list = []

		if sessions is not None:

			for session in sessions:

				list_of_questions = get_list(session.questions)

				questions_list = []

				for question in list_of_questions:

					questions = Questions.query.get(int(question))

					questions_dict = {
					'question': questions.question
					}

					questions_list.append(questions_dict)

				session_dict = {
					'time': session.time,
					'guess': session.guess,
					'found': session.found,
					'accepted': session.accepted,
					'questions': questions_list,
					'answers': get_list(session.answers)
				}

				sessions_list.append(session_dict)					

			return jsonify(sessions_list)

		else:

			return jsonify({'error': 'norecords'})


	else:
			abort(403)


# Start Game
@game.route('/api/v1/correct_guess', methods=['POST', 'GET'])
def correct_guess():

	if request.method == 'POST':

		if f"{request_source}guess" in request.headers.get("Referer"):

			data = request.get_json(silent=True)

			questions = str(data.get('questions'))
			answers = str(data.get('answers'))
			guess = data.get('guess')
			found = 1
			accepted = 1

			new_session = Sessions(questions=questions, answers=answers, guess=guess, found=found, accepted=accepted)
			db.session.add(new_session)
			db.session.commit()
			return jsonify({
				'message': 'done'
				})

		else:
			abort(403)

	else:
			abort(403)

# Start Game
@game.route('/api/v1/wrong_guess', methods=['POST', 'GET'])
def wrong_guess():

	if request.method == 'POST':

		if f"{request_source}guess" in request.headers.get("Referer"):

			data = request.get_json(silent=True)

			questions = str(data.get('questions'))
			answers = str(data.get('answers'))
			guess = data.get('guess')
			found = 1
			accepted = 0

			new_session = Sessions(questions=questions, answers=answers, guess=guess, found=found, accepted=accepted)
			db.session.add(new_session)
			db.session.commit()
			return jsonify({
				'message': 'done'
				})

		else:
			abort(403)

	else:
			abort(403)
			
