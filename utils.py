# 将SQLAlchemy模型对象转换成字典
def model_to_dict(model_instance):
  return {
    column.name: getattr(model_instance, column.name)
    for column in model_instance.__table__.columns
  }

# 重复检查
def check_duplicate_value(model, field, value):
  try:
    # existing_catecory = DishType.query.filter_by(name=data["name"]).first()
    exsisting_record = model.query.filter_by(**{field: value}).first()
    if exsisting_record:
      return True
    return False
  except Exception as e:
    print(f"Error checking duplicate: {e}")
    return False