from flask.ext.sqlalchemy import SQLAlchemy




db = SQLAlchemy()

class Drink(db.Model):
	uid = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	president = db.Column(db.String(100))


	def __init__(self, name, president):
		self.name = name.title()
		self.president = name.title()

