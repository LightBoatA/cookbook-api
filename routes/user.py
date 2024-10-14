from flask import Blueprint, request, jsonify
from models import User, db
from utils import model_to_dict, check_duplicate_value

user_bp = Blueprint('user', __name__)

# 获取所有用户
@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([model_to_dict(user) for user in users])

# 创建用户
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # 判重，检查是否有重复的用户名
    if check_duplicate_value(User, "username", data["username"]):
        return jsonify({'error': '用户名已存在'}), 400
    
    # 创建新用户
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'username': new_user.username}), 201

# 更新用户信息
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id, description="User not found")
    data = request.get_json()
    
    # 判重，检查是否有重复的用户名
    if check_duplicate_value(User, "username", data["username"]):
        return jsonify({'error': '用户名已存在'}), 400
    
    # 更新用户数据
    for key, value in data.items():
        if key != "id":
            setattr(user, key, value)
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# 删除用户
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id, description="User not found")
    
    # 删除用户
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 204
