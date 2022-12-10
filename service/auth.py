import datetime
import calendar
import jwt

from constants import JWT_SECRET, JWT_ALGORITHM
from flask_restx import abort
from service.user import UserService


class AuthService:
	def __init__(self, user_service: UserService):
		self.user_service = user_service

	def generate_tokens(self, email, password, is_refresh=False):
		user = self.user_service.get_by_email(email)

		if user is None:
			raise abort(404)

		if not is_refresh:
			if not self.user_service.compare_passwords(user.password, password):
				abort(400)

		user.email = str(email)

		data = {
			"username": user.username,
			"role": user.role
		}

		# 60 minutes for access token
		access_token_lifetime = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
		data["exp"] = calendar.timegm(access_token_lifetime.timetuple())
		access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

		# 90 days for refresh token
		refresh_token_lifetime = datetime.datetime.utcnow() + datetime.timedelta(days=90)
		data["exp"] = calendar.timegm(refresh_token_lifetime.timetuple())
		refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

		return {
			"access_token": access_token,
			"refresh_token": refresh_token
		}

	def approve_tokens(self, access_token, refresh_token):
		data_a = jwt.decode(jwt=access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
		data_r = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])

		if data_a["username"] != data_r["username"]:
			raise abort(404)

		username = data_a.get("username")
		user = self.user_service.get_by_username(username)

		email = user.email

		if user is None:
			raise abort(404)

		return self.generate_tokens(email, None, is_refresh=True)
