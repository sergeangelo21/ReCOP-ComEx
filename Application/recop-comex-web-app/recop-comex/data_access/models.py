from extensions import db

class user(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable = False)
	password = db.Column(db.String(30), nullable = False)

	def __repr__(self):
		return '<user {}>' .format(self.username)