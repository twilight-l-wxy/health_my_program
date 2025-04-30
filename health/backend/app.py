from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # 启用CORS支持跨域请求

# 配置
app.config.from_object('config')

# 路由
@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': '智医通API服务正在运行'
    })

# 用户认证API
@app.route('/api/auth/register', methods=['POST'])
def register():
    # 这里将实现用户注册逻辑
    return jsonify({
        'status': 'success',
        'message': '用户注册成功'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    # 这里将实现用户登录逻辑
    return jsonify({
        'status': 'success',
        'message': '用户登录成功',
        'data': {
            'token': 'sample_token',
            'user': {
                'id': 1,
                'username': 'test_user',
                'role': 'user'
            }
        }
    })

# 症状自查API
@app.route('/api/symptom/check', methods=['POST'])
def symptom_check():
    # 这里将实现症状初步检查逻辑
    return jsonify({
        'status': 'success',
        'message': '症状已接收',
        'data': {
            'consultation_id': 1,
            'next_question': '您的症状持续了多长时间？'
        }
    })

@app.route('/api/symptom/questions', methods=['GET'])
def get_questions():
    # 这里将实现获取问诊问题逻辑
    consultation_id = request.args.get('consultation_id')
    return jsonify({
        'status': 'success',
        'data': {
            'questions': [
                {
                    'id': 1,
                    'text': '您的症状持续了多长时间？',
                    'type': 'choice',
                    'options': ['不到24小时', '1-3天', '4-7天', '一周以上', '一个月以上']
                }
            ]
        }
    })

@app.route('/api/symptom/answer', methods=['POST'])
def submit_answer():
    # 这里将实现提交问题回答逻辑
    return jsonify({
        'status': 'success',
        'message': '回答已接收',
        'data': {
            'next_question': '您是否有发热症状？',
            'is_last': False
        }
    })

@app.route('/api/symptom/result', methods=['GET'])
def get_result():
    # 这里将实现获取自查结果逻辑
    consultation_id = request.args.get('consultation_id')
    return jsonify({
        'status': 'success',
        'data': {
            'possible_diseases': [
                {
                    'name': '普通感冒',
                    'probability': 0.75,
                    'description': '普通感冒是一种常见的上呼吸道感染，通常由病毒引起。'
                },
                {
                    'name': '流行性感冒',
                    'probability': 0.25,
                    'description': '流行性感冒是由流感病毒引起的急性呼吸道传染病。'
                }
            ],
            'risk_level': '低',
            'recommended_department': '呼吸内科',
            'advice': '建议多休息，多喝水，如症状加重请及时就医。'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)