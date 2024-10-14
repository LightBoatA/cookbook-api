from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)

class DishType(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(10), unique=True, nullable=False)

class Dish(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(10), nullable=False)
  description = db.Column(db.String(50), nullable=True)
  recipe = db.Column(db.String(500), nullable=True)
  image = db.Column(db.String(200), nullable=True)

  type_id = db.Column(db.Integer, db.ForeignKey('dish_type.id'), nullable=False)
  type = db.relationship('DishType', backref=db.backref('dishes', lazy=True))

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', backref=db.backref('dishes', lazy=True))