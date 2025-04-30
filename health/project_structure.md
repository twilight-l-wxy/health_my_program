# 智医通项目结构设计

## 目录结构

```
/health
├── frontend/                # 前端代码
│   ├── public/              # 静态资源
│   │   ├── favicon.ico      # 网站图标
│   │   └── index.html       # HTML模板
│   ├── src/                 # 源代码
│   │   ├── components/      # 组件
│   │   │   ├── common/      # 通用组件
│   │   │   ├── layout/      # 布局组件
│   │   │   └── symptom/     # 症状相关组件
│   │   ├── pages/           # 页面
│   │   │   ├── user/        # 用户端页面
│   │   │   ├── doctor/      # 医生端页面
│   │   │   └── admin/       # 管理端页面
│   │   ├── services/        # API服务
│   │   ├── utils/           # 工具函数
│   │   ├── store/           # Redux状态管理
│   │   ├── App.jsx          # 主应用
│   │   └── main.jsx         # 入口文件
│   ├── package.json         # 依赖配置
│   └── vite.config.js       # Vite配置
├── backend/                 # 后端代码
│   ├── api/                 # API接口
│   │   ├── user.py          # 用户相关API
│   │   ├── symptom.py       # 症状相关API
│   │   ├── diagnosis.py     # 诊断相关API
│   │   └── admin.py         # 管理相关API
│   ├── models/              # 数据模型
│   │   ├── user.py          # 用户模型
│   │   ├── symptom.py       # 症状模型
│   │   └── diagnosis.py     # 诊断模型
│   ├── services/            # 业务逻辑
│   │   ├── auth.py          # 认证服务
│   │   ├── symptom.py       # 症状服务
│   │   └── diagnosis.py     # 诊断服务
│   ├── utils/               # 工具函数
│   │   ├── db.py            # 数据库工具
│   │   └── logger.py        # 日志工具
│   ├── app.py               # 主应用
│   ├── config.py            # 配置文件
│   └── requirements.txt     # 依赖配置
├── ai_model/                # AI模型
│   ├── data/                # 训练数据
│   │   ├── raw/             # 原始数据
│   │   └── processed/       # 处理后的数据
│   ├── models/              # 模型文件
│   │   ├── base_model/      # 基础模型
│   │   └── fine_tuned/      # 微调模型
│   ├── training/            # 训练脚本
│   │   ├── train.py         # 训练主脚本
│   │   └── evaluate.py      # 评估脚本
│   └── inference/           # 推理脚本
│       ├── symptom_recognition.py  # 症状识别
│       └── risk_assessment.py      # 风险评估
├── docs/                    # 文档
│   ├── api/                 # API文档
│   ├── database/            # 数据库设计
│   │   ├── schema.md        # 数据库模式
│   │   └── er_diagram.md    # ER图
│   └── deployment/          # 部署文档
├── scripts/                 # 脚本
│   ├── setup.sh             # 环境设置脚本
│   └── deploy.sh            # 部署脚本
└── README.md                # 项目说明
```

## 数据库设计

### 用户表 (users)
- id: 主键
- username: 用户名
- password: 密码（加密存储）
- email: 邮箱
- phone: 手机号
- role: 角色（用户/医生/管理员）
- created_at: 创建时间
- updated_at: 更新时间

### 患者信息表 (patient_profiles)
- id: 主键
- user_id: 用户ID（外键）
- name: 姓名
- gender: 性别
- birth_date: 出生日期
- height: 身高
- weight: 体重
- blood_type: 血型
- allergies: 过敏史
- chronic_diseases: 慢性病史
- family_history: 家族病史

### 医生信息表 (doctor_profiles)
- id: 主键
- user_id: 用户ID（外键）
- name: 姓名
- gender: 性别
- title: 职称
- department: 科室
- hospital: 医院
- license_number: 执业证号
- specialties: 专长
- introduction: 简介

### 症状表 (symptoms)
- id: 主键
- name: 症状名称
- description: 描述
- keywords: 关键词（用于搜索）
- body_part: 身体部位
- severity_levels: 严重程度级别
- common_causes: 常见原因

### 疾病表 (diseases)
- id: 主键
- name: 疾病名称
- icd_code: ICD-10编码
- description: 描述
- symptoms: 相关症状（多对多）
- risk_factors: 风险因素
- prevention: 预防措施
- treatment: 治疗方法
- department: 就诊科室

### 问诊记录表 (consultations)
- id: 主键
- patient_id: 患者ID（外键）
- created_at: 创建时间
- chief_complaint: 主诉
- symptom_description: 症状描述
- duration: 持续时间
- severity: 严重程度
- status: 状态（进行中/已完成）

### 问诊问答表 (consultation_qa)
- id: 主键
- consultation_id: 问诊ID（外键）
- question: 问题
- answer: 回答
- sequence: 序号
- created_at: 创建时间

### 诊断结果表 (diagnoses)
- id: 主键
- consultation_id: 问诊ID（外键）
- possible_diseases: 可能疾病（JSON格式，包含疾病ID和概率）
- risk_level: 风险等级（低/中/高）
- recommended_department: 推荐科室
- advice: 建议
- created_at: 创建时间

## API设计

### 用户API
- POST /api/auth/register - 用户注册
- POST /api/auth/login - 用户登录
- GET /api/auth/profile - 获取用户资料
- PUT /api/auth/profile - 更新用户资料
- POST /api/auth/logout - 用户登出

### 患者API
- GET /api/patient/profile - 获取患者资料
- PUT /api/patient/profile - 更新患者资料
- GET /api/patient/consultations - 获取问诊历史
- GET /api/patient/consultation/{id} - 获取问诊详情

### 医生API
- GET /api/doctor/profile - 获取医生资料
- PUT /api/doctor/profile - 更新医生资料
- GET /api/doctor/patients - 获取患者列表
- GET /api/doctor/consultations - 获取问诊列表

### 症状自查API
- POST /api/symptom/check - 提交症状自查
- GET /api/symptom/questions - 获取问诊问题
- POST /api/symptom/answer - 提交问题回答
- GET /api/symptom/result - 获取自查结果

### 管理API
- GET /api/admin/users - 获取用户列表
- GET /api/admin/doctors - 获取医生列表
- GET /api/admin/symptoms - 获取症状列表
- POST /api/admin/symptom - 添加症状
- PUT /api/admin/symptom/{id} - 更新症状
- DELETE /api/admin/symptom/{id} - 删除症状

## 前端页面设计

### 用户端
- 首页 - 展示系统介绍和功能入口
- 注册/登录页 - 用户注册和登录
- 症状自查页 - 输入症状并进行自查
- 问诊流程页 - 回答系统提问
- 结果页 - 显示自查结果和建议
- 历史记录页 - 查看历史自查记录
- 个人中心 - 管理个人资料

### 医生端
- 工作台 - 显示待处理问诊和统计信息
- 患者管理 - 管理患者信息
- 问诊辅助 - AI辅助问诊工具
- 数据分析 - 分析问诊数据和趋势

### 管理端
- 仪表盘 - 显示系统运行状态和统计信息
- 用户管理 - 管理用户账号
- 医生管理 - 管理医生账号
- 知识库管理 - 管理症状和疾病数据
- 系统设置 - 配置系统参数

## 技术实现要点

### 症状识别模块
- 使用BiLSTM-CRF模型识别用户描述中的症状关键词
- 构建症状同义词库，解决症状描述的多样性问题
- 实现模糊匹配算法，处理拼写错误和不规范表述

### 问诊引擎模块
- 基于有限状态机模型设计问诊流程
- 使用决策树算法确定下一个问题
- 控制问诊轮次不超过5轮，平衡深度与效率

### 风险评估模块
- 使用贝叶斯网络计算疾病概率
- 设置三级预警阈值（低/中/高）
- 结合患者基本信息进行个性化风险评估

### 模型轻量化
- 使用知识蒸馏技术压缩模型
- 应用量化和剪枝技术减小模型体积
- 优化推理速度至2s/次以内

## 部署方案

### 开发环境
- 前端：Node.js + npm
- 后端：Python 3.8+
- 数据库：MySQL 8.0
- AI模型：PyTorch 1.10+

### 生产环境
- 前端：Nginx + React静态文件
- 后端：Gunicorn + Flask
- 数据库：MySQL主从复制
- AI模型：ONNX Runtime部署

### 部署步骤
1. 准备服务器环境
2. 配置数据库
3. 部署后端API服务
4. 部署AI模型服务
5. 部署前端静态文件
6. 配置Nginx反向代理
7. 设置监控和日志
8. 进行性能测试和优化