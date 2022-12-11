from dao.model.user import User


class UserDAO:
	def __init__(self, session):
		self.session = session

	def get_one(self, uid):
		return self.session.query(User).get(uid)

	def get_all(self):
		return self.session.query(User).all()

	def get_by_username(self, username):
		return self.session.query(User).filter(User.username == username).first()

	def get_by_email(self, email):
		return self.session.query(User).filter(User.email == email).first()

	def create(self, user_d):
		# new_user = User(
		# 	id=user_d.get('id'),
		# 	username=user_d.get('username'),
		# 	password=user_d.get('password'),
		# 	role=user_d.get('role')
		# )
		new_user = User(
			id=user_d.get('id'),
			email=user_d.get('email'),
			password=user_d.get('password'),
			name=user_d.get('name'),
			surname=user_d.get('surname'),
			favorite_genre=user_d.get('favorite_genre'),
			username=user_d.get('username'),
			role=user_d.get('role')
		)

		self.session.add(new_user)
		self.session.commit()
		return new_user

	def delete(self, uid):
		user = self.get_one(uid)
		self.session.delete(user)
		self.session.commit()

	def update(self, user, user_info):
		user = self.get_one(user["id"])

		user.name = user_info["name"]
		user.username = user_info["username"]
		user.surname = user_info["surname"]
		user.role = user_info["role"]
		user.favorite_genre = user_info["favorite_genre"]

		self.session.add(user)
		self.session.commit()

	def update_password(self, user, password):
		user.password = password

		self.session.add(user)
		self.session.commit()

	# def update(self, user_d):
	# 	user = self.get_one(user_d.get("id"))
	# 	user.username = user_d.get("username")
	# 	user.password = user_d.get("password")
	# 	user.role = user_d.get("role")
	# 	user.surname = user_d.get("surname")
	# 	user.email = user_d.get("email")
	# 	user.favorite_genre = user_d.get("favorite_genre")
	# 	user.name = user_d.get("name")
	#
	# 	self.session.add(user)
	# 	self.session.commit()
