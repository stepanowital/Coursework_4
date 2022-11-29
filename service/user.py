import hashlib
import base64
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
	def __init__(self, dao: UserDAO):
		self.dao = dao

	def get_one(self, uid):
		return self.dao.get_one(uid)

	def get_all(self):
		return self.dao.get_all()

	def get_by_username(self, username):
		return self.dao.get_by_username(username)

	def create(self, user_d):
		user_d["password"] = self.generate_password(user_d.get("password"))
		return self.dao.create(user_d)

	def update(self, user_d):
		user_d["password"] = self.generate_password(user_d.get("password"))
		return self.dao.update(user_d)

	def delete(self, uid):
		self.dao.delete(uid)

	def generate_password(self, password):
		return base64.b64encode(hashlib.pbkdf2_hmac(
			'sha256',
			password.encode('utf-8'),  # Convert the password to bytes
			PWD_HASH_SALT,
			PWD_HASH_ITERATIONS
		))

	def compare_passwords(self, password_hash, other_password) -> bool:
		decoded_digest = base64.b64decode(password_hash)

		hash_digest = hashlib.pbkdf2_hmac(
			'sha256',
			other_password.encode('utf-8'),
			PWD_HASH_SALT,
			PWD_HASH_ITERATIONS
		)

		return hmac.compare_digest(decoded_digest, hash_digest)
