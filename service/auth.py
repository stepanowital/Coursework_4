import datetime
import calendar
import jwt

from constants import JWT_SECRET, JWT_ALGORITHM
from flask_restx import abort
from service.user import UserService


class AuthService:
	def __init__(self, user_service: UserService):
		self.user_service = user_service

	def generate_tokens(self, username, password, is_refresh=False):
		user = self.user_service.get_by_username(username)

		if user is None:
			raise abort(404)

		if not is_refresh:
			if not self.user_service.compare_passwords(user.password, password):
				abort(400)

		data = {
			"username": user.username,
			"role": user.role
		}

		# 30 minutes for access token
		access_token_lifetime = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
		data["exp"] = calendar.timegm(access_token_lifetime.timetuple())
		access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

		# 130 days for refresh token
		refresh_token_lifetime = datetime.datetime.utcnow() + datetime.timedelta(days=90)
		data["exp"] = calendar.timegm(refresh_token_lifetime.timetuple())
		refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

		return {
			"access_token": access_token,
			"refresh_token": refresh_token
		}

	def approve_refresh_token(self, refresh_token):
		data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
		username = data.get("username")

		user = self.user_service.get_by_username(username)

		if user is None:
			raise abort(404)

		return self.generate_tokens(username, None, is_refresh=True)
