from flask.ext.sqlalchemy import SQLAlchemy




db = SQLAlchemy()

class Drink(db.Model):
	uid = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	president = db.Column(db.String(100))
	ingredients = db.relationship('Ingredient', backref='drink', lazy='dynamic')



	def __init__(self, name, president, ingredient):
		self.name = name.title()
		self.president = president.title()
		self.ingredient = ingredient



class Ingredient(db.Model):
	uid = db.Column(db.Integer, primary_key= True)
	number = db.Column(db.Integer)
	desc = db.Column(db.String(512))
	drink_id = db.Column(db.Integer, db.ForeignKey('drink.uid'))

	def __init__(self, number, desc):
		self.number = number
		self.desc = desc



