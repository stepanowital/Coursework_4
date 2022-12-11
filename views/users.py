import jwt
from flask import request
from flask_restx import Resource, Namespace

from constants import JWT_SECRET, JWT_ALGORITHM
from dao.model.user import UserSchema
from decorators import auth_required
from implemented import user_service

users_ns = Namespace('users')
user_ns = Namespace('user')


@user_ns.route('/')
class UserViews(Resource):
	@auth_required
	def get(self):
		token_data = request.headers["Authorization"]
		token = token_data.split("Bearer ")[-1]
		user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
		user = user_service.get_one(user["id"])
		user_info = UserSchema().dump(user)
		return user_info, 200

	@auth_required
	def patch(self):
		user_info = request.json

		token_data = request.headers["Authorization"]
		token = token_data.split("Bearer ")[-1]
		user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

		user_service.update(user, user_info)

		return "Данные пользователя обновлены", 204


@user_ns.route('/password')
class UsersViews(Resource):
	@auth_required
	def put(self):
		req_json = request.json
		password_1 = req_json.get("password_1")
		password_2 = req_json.get("password_2")

		token_data = request.headers["Authorization"]
		token = token_data.split("Bearer ")[-1]
		user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
		user_d = user_service.get_one(user["id"])

		if not user_service.compare_passwords(user_d.password, password_1):
			return "Password_1 неверный", 401

		password_2_hash = user_service.generate_password(password_2)

		user_service.update_password(user_d, password_2_hash)

		return "Пароль обновлён", 204




@users_ns.route('/')
class UsersView(Resource):
	def get(self):
		rs = user_service.get_all()
		res = UserSchema(many=True).dump(rs)
		return res, 200

	def post(self):
		req_json = request.json
		user = user_service.create(req_json)
		return "", 201, {"location": f"/users/{user.id}"}


@users_ns.route('/<int:uid>')
class UserView(Resource):
	def get(self, uid):
		r = user_service.get_one(uid)
		sm_d = UserSchema().dump(r)
		return sm_d, 200

	def patch(self, uid):
		req_json = request.json
		if "id" not in req_json:
			req_json["id"] = uid
		user_service.update(req_json)
		return "", 204

	def delete(self, uid):
		user_service.delete(uid)
		return "", 204
