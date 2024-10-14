from flask import Blueprint, request,jsonify
from models import DishType, Dish, db
from utils import model_to_dict, check_duplicate_value
from constants import DEFAULT_CATEGORY

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
def get_all_categories():
    categories = DishType.query.all()
    return jsonify([model_to_dict(c) for c in categories])

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    # 判重
    if check_duplicate_value(DishType, "name", data["name"]):
      return jsonify({'error': '种类名已存在'}), 400
    
    # 没有重复，创建新的类别
    new_category = DishType(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully', 'category': new_category.name}), 201

@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
  category = DishType.query.get_or_404(category_id, description="Category not found")
  data = request.get_json()
  # 判重
  if check_duplicate_value(DishType, "name", data["name"]):
    return jsonify({'error': '种类名已存在'}), 400
  # 更新
  for key, value in data.items(): # 字典.items方法，返回字典中每个对象的元组
    if key != "id":
      setattr(category, key, value) # python内置方法，设置对象对应键的值
  db.session.commit()
  return jsonify({'message': 'Category update successfully'})

@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    # 获取要删除的 DishType
    dish_type = DishType.query.get_or_404(category_id, description="DishType not found")

    # 防止删除 "默认" 分类
    if dish_type.name == DEFAULT_CATEGORY:
        return jsonify({'error': 'Cannot delete the default category.'}), 400

    # 查询是否有任何 Dish 与该 DishType 关联
    associated_dishes = Dish.query.filter_by(type_id=category_id).all()

    if associated_dishes:
        # 查找 "默认" 分类的 ID
        default_type = DishType.query.filter_by(name=DEFAULT_CATEGORY).first()

        # 如果没有找到 "默认" 分类，返回错误（这种情况不太可能发生）
        if not default_type:
          return jsonify({'error': 'Default category not found.'}), 500

        # 将所有关联的菜品的 type_id 改为 "默认" 分类的 ID
        for dish in associated_dishes:
          dish.type_id = default_type.id
        db.session.commit()

    # 如果没有关联的 Dish，删除 DishType
    db.session.delete(dish_type)
    db.session.commit()

    return jsonify({'message': 'DishType deleted successfully'}), 204
