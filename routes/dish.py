from flask import Blueprint, request,jsonify, current_app, send_from_directory
from models import Dish, db
from utils import model_to_dict
from werkzeug.utils import secure_filename
import os
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 检查文件扩展名是否合法
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(extension):
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{extension}"

# 设置上传文件的存储路径
# current_app.config['UPLOAD_FOLDER'] = os.path.join(current_app.root_path, 'uploads')

dish_bp = Blueprint('dish', __name__)

@dish_bp.route('/', methods=['POST'])
def create_dish():
  data = request.get_json()
  new_dish = Dish(
    name=data['name'],
    description=data['description'],
    recipe=data['recipe'],
    image=data['image'],
    type_id=data['type_id'],
    user_id=data['user_id']
  )
  db.session.add(new_dish)
  db.session.commit()
  return jsonify({'message': 'Dish created successfully', 'name': new_dish.name}), 201

@dish_bp.route('/')
def get_dishes():
  user_id = request.args.get("user_id")
  if user_id:
    dishes = Dish.query.filter_by(user_id=user_id).all()
  else:
    dishes = Dish.query.all()
  return jsonify([model_to_dict(dish) for dish in dishes])

@dish_bp.route('/<int:dish_id>')
def get_dish(dish_id):
  dish = dish = Dish.query.get_or_404(dish_id, description="Dish not found")
  return jsonify(model_to_dict(dish))

@dish_bp.route('/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
  dish = dish = Dish.query.get_or_404(dish_id, description="Dish not found")
  data = request.get_json()
  for key, value in data.items(): # 字典.items方法，返回字典中每个对象的元组
    if key != "id":
      setattr(dish, key, value) # python内置方法，设置对象对应键的值
  db.session.commit()
  return jsonify({'message': 'Dish update successfully'})

@dish_bp.route('/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
  dish = dish = Dish.query.get_or_404(dish_id, description="Dish not found")
  db.session.delete(dish)
  db.session.commit()
  return jsonify({'message': 'Delete successfully'}), 204


@dish_bp.route('/upload', methods=['POST'])
def upload_image():
    print(request.files)
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400
    file = request.files['image']

    if file and allowed_file(file.filename):
        # 获取文件扩展名
        _, extension = os.path.splitext(file.filename)
        # 生成唯一文件名
        filename = generate_unique_filename(extension)

        # 文件保存路径
        upload_folder = current_app.config['UPLOAD_FOLDER']
        # upload_folder = os.path.join(current_app.root_path, 'uploads')
        
        # 如果文件夹不存在，创建它
        # if not os.path.exists(upload_folder):
        #     os.makedirs(upload_folder)

        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # 返回文件路径（相对服务器根目录的路径）
        return jsonify({
            'message': 'File uploaded successfully',
            # 'location': f'/uploads/{filename}'
            'location': f'/{filename}'
        }), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

# 静态文件接口
# @dish_bp.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
