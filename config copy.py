import os

class Config:
  # os.path.dirname(__file__) 获取当前脚本所在文件的目录路径
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'data.db')
  # 关闭数据库事件系统，节约资源
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  # 用于绘画管理和认证
  SECRET_KEY = os.urandom(24)