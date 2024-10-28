import os

class Config:
  # 获取当前脚本所在的文件夹路径
  BASE_DIR = os.path.dirname(__file__)

  # 数据库配置
  # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'data.db')
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:qwe123!!!QWE@47.101.148.6:3306/cookbook'
  # 关闭数据库事件系统，节约资源
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  
  # 安全管理，用于绘画管理和认证
  SECRET_KEY = os.urandom(24)

  # 上传文件夹配置
  UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')