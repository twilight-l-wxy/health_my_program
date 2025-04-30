# 智医通后端配置文件

import os

# 基本配置
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_for_development_only')

# 数据库配置
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///zhiyitong.db')

# JWT配置
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt_dev_key_for_development_only')
JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时

# AI模型配置
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_model/models/fine_tuned')
MODEL_NAME = 'llama-3-8b-quantized'
MAX_QUESTION_ROUNDS = 5  # 最大问诊轮次

# 风险评估阈值
RISK_THRESHOLD_LOW = 0.3
RISK_THRESHOLD_MEDIUM = 0.6
# 高风险阈值 > 0.6

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/app.log'

# 跨域配置
CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']