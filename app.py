from flask import Flask, send_from_directory
from config import Config
from models import DishType, db
from routes.dish import dish_bp
from routes.category import category_bp
from routes.auth import auth_bp
from routes.user import user_bp
from flask_migrate import Migrate
from constants import DEFAULT_CATEGORY
from flask_cors import CORS
import os

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
# 创建上传文件夹（如果不存在）
if not os.path.exists(app.config['UPLOAD_FOLDER']):
  os.makedirs(app.config['UPLOAD_FOLDER'])

# 初始化数据库
db.init_app(app) 

# 初始化 Flask-Migrate 进行数据库迁移
Migrate = Migrate(app, db)

# 创建数据库和表
with app.app_context():
  # 创建默认分类
  # db.create_all()
  # print('创建表')
  def create_default_dish_type():
    default_type = DishType.query.filter_by(name=DEFAULT_CATEGORY).first()
    if not default_type:
      default_type = DishType(name=DEFAULT_CATEGORY)
      db.session.add(default_type)
      db.session.commit()

  create_default_dish_type()
  # db.create_all()

# 注册蓝图
app.register_blueprint(dish_bp, url_prefix='/api/dish')
app.register_blueprint(category_bp, url_prefix='/api/category')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')

# 访问上传文件
@app.route('/file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
  app.run(debug=True)