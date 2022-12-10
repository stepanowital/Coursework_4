from flask import request
from flask_restx import Resource, Namespace
from implemented import auth_service, user_service

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthsRegister(Resource):
	def post(self):
		req_json = request.json
		user = user_service.create(req_json)
		return "", 201, {"location": f"/users/{user.id}"}


@auth_ns.route('/login/')
class AuthsLogin(Resource):
	def post(self):
		req_json = request.json
		email = req_json.get('email', None)
		password = req_json.get('password', None)

		if None in [email, password]:
			return "", 401

		tokens = auth_service.generate_tokens(email, password)
		return tokens, 201

	def put(self):
		req_json = request.json
		access_token = req_json.get('access_token')
		refresh_token = req_json.get('refresh_token')

		if refresh_token is None or access_token is None:
			return "", 401

		tokens = auth_service.approve_tokens(access_token, refresh_token)
		return tokens, 201
