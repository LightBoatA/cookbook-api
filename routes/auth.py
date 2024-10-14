from flask import Blueprint, request, jsonify
from models import User, db
from utils import check_duplicate_value

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  if check_duplicate_value(User, "username", data["username"]):
    return jsonify({'error': 'Username already exists'}), 400
  new_user = User(username=data['username'])
  db.session.add(new_user)
  db.session.commit()
  return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  user = User.query.filter_by(username=data['username']).first()
  if not user:
    return jsonify({'error': 'User not found'}), 404
  return jsonify({'message': 'Login successful', 'user': user.username}), 200
