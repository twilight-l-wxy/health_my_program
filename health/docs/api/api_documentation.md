# 智医通API文档

## API概述

智医通系统采用RESTful API设计风格，所有API均返回JSON格式数据。API基础URL为`/api`，所有请求和响应均使用UTF-8编码。

## 通用响应格式

```json
{
  "status": "success", // 或 "error"
  "message": "操作成功", // 或错误信息
  "data": {}, // 响应数据，错误时可能为null
  "error_code": null // 错误时的错误代码，成功时为null
}
```

## 认证机制

除了少数公开API外，大多数API需要认证才能访问。认证采用JWT (JSON Web Token)机制，客户端需要在HTTP请求头中添加`Authorization`字段：

```
Authorization: Bearer {token}
```

## API列表

### 1. 用户认证API

#### 1.1 用户注册

- **URL**: `/api/auth/register`
- **方法**: POST
- **描述**: 注册新用户
- **请求参数**:

```json
{
  "username": "user123",
  "password": "securepassword",
  "email": "user@example.com",
  "phone": "13800138000"
}
```

- **响应示例**:

```json
{
  "status": "success",
  "message": "用户注册成功",
  "data": {
    "user_id": 1,
    "username": "user123"
  }
}
```

#### 1.2 用户登录

- **URL**: `/api/auth/login`
- **方法**: POST
- **描述**: 用户登录并获取访问令牌
- **请求参数**:

```json
{
  "username": "user123",
  "password": "securepassword"
}
```

- **响应示例**:

```json
{
  "status": "success",
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "user123",
      "role": "user"
    }
  }
}
```

#### 1.3 获取用户资料

- **URL**: `/api/auth/profile`
- **方法**: GET
- **描述**: 获取当前登录用户的资料
- **请求头**: 需要包含有效的JWT令牌
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "user": {
      "id": 1,
      "username": "user123",
      "email": "user@example.com",
      "phone": "13800138000",
      "role": "user",
      "created_at": "2023-01-01T12:00:00Z"
    }
  }
}
```

#### 1.4 更新用户资料

- **URL**: `/api/auth/profile`
- **方法**: PUT
- **描述**: 更新当前登录用户的资料
- **请求头**: 需要包含有效的JWT令牌
- **请求参数**:

```json
{
  "email": "newemail@example.com",
  "phone": "13900139000"
}
```

- **响应示例**:

```json
{
  "status": "success",
  "message": "资料更新成功",
  "data": {
    "user": {
      "id": 1,
      "username": "user123",
      "email": "newemail@example.com",
      "phone": "13900139000"
    }
  }
}
```

### 2. 患者API

#### 2.1 获取患者资料

- **URL**: `/api/patient/profile`
- **方法**: GET
- **描述**: 获取当前登录用户的患者资料
- **请求头**: 需要包含有效的JWT令牌
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "profile": {
      "id": 1,
      "user_id": 1,
      "name": "张三",
      "gender": "male",
      "birth_date": "1990-01-01",
      "height": 175,
      "weight": 70,
      "blood_type": "A",
      "allergies": "花粉过敏",
      "chronic_diseases": "无",
      "family_history": "父亲有高血压史"
    }
  }
}
```

#### 2.2 更新患者资料

- **URL**: `/api/patient/profile`
- **方法**: PUT
- **描述**: 更新当前登录用户的患者资料
- **请求头**: 需要包含有效的JWT令牌
- **请求参数**:

```json
{
  "name": "张三",
  "gender": "male",
  "birth_date": "1990-01-01",
  "height": 175,
  "weight": 70,
  "blood_type": "A",
  "allergies": "花粉过敏",
  "chronic_diseases": "无",
  "family_history": "父亲有高血压史"
}
```

- **响应示例**:

```json
{
  "status": "success",
  "message": "患者资料更新成功",
  "data": {
    "profile_id": 1
  }
}
```

#### 2.3 获取问诊历史

- **URL**: `/api/patient/consultations`
- **方法**: GET
- **描述**: 获取当前登录用户的问诊历史
- **请求头**: 需要包含有效的JWT令牌
- **查询参数**:
  - `page`: 页码，默认为1
  - `limit`: 每页记录数，默认为10
  - `status`: 问诊状态筛选，可选值为`in_progress`、`completed`、`cancelled`，默认为全部
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "consultations": [
      {
        "id": 1,
        "created_at": "2023-03-01T14:30:00Z",
        "chief_complaint": "头痛、发热",
        "status": "completed",
        "completed_at": "2023-03-01T15:00:00Z"
      },
      {
        "id": 2,
        "created_at": "2023-03-10T09:15:00Z",
        "chief_complaint": "咳嗽、咽痛",
        "status": "completed",
        "completed_at": "2023-03-10T09:45:00Z"
      }
    ],
    "pagination": {
      "total": 2,
      "page": 1,
      "limit": 10,
      "pages": 1
    }
  }
}
```

### 3. 症状自查API

#### 3.1 提交症状自查

- **URL**: `/api/symptom/check`
- **方法**: POST
- **描述**: 提交初始症状描述，开始自查流程
- **请求头**: 需要包含有效的JWT令牌
- **请求参数**:

```json
{
  "chief_complaint": "头痛三天，伴有轻微发热",
  "symptom_description": "额头疼痛，按压时加重，体温37.5度，没有其他不适",
  "duration": "3天"
}
```

- **响应示例**:

```json
{
  "status": "success",
  "message": "症状已接收",
  "data": {
    "consultation_id": 3,
    "next_question": "您的头痛是持续性的还是间歇性的？"
  }
}
```

#### 3.2 获取问诊问题

- **URL**: `/api/symptom/questions`
- **方法**: GET
- **描述**: 获取下一个问诊问题
- **请求头**: 需要包含有效的JWT令牌
- **查询参数**:
  - `consultation_id`: 问诊ID
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "questions": [
      {
        "id": 1,
        "text": "您的头痛是持续性的还是间歇性的？",
        "type": "choice",
        "options": ["持续性", "间歇性"]
      }
    ],
    "progress": {
      "current": 1,
      "total": 5
    }
  }
}
```

#### 3.3 提交问题回答

- **URL**: `/api/symptom/answer`
- **方法**: POST
- **描述**: 提交问题的回答
- **请求头**: 需要包含有效的JWT令牌
- **请求参数**:

```json
{
  "consultation_id": 3,
  "question_id": 1,
  "answer": "间歇性"
}
```

- **响应示例**:

```json
{
  "status": "success",
  "message": "回答已接收",
  "data": {
    "next_question": "头痛发作时，疼痛程度如何？",
    "is_last": false
  }
}
```

#### 3.4 获取自查结果

- **URL**: `/api/symptom/result`
- **方法**: GET
- **描述**: 获取症状自查的结果
- **请求头**: 需要包含有效的JWT令牌
- **查询参数**:
  - `consultation_id`: 问诊ID
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "possible_diseases": [
      {
        "name": "偏头痛",
        "probability": 0.65,
        "description": "偏头痛是一种常见的神经血管性疾病，特点是反复发作的中重度、搏动性头痛。"
      },
      {
        "name": "紧张性头痛",
        "probability": 0.25,
        "description": "紧张性头痛是最常见的原发性头痛，通常表现为双侧压迫感或紧箍感。"
      },
      {
        "name": "鼻窦炎",
        "probability": 0.10,
        "description": "鼻窦炎是鼻窦黏膜的炎症，可引起头痛、鼻塞和面部压力感。"
      }
    ],
    "risk_level": "低",
    "recommended_department": "神经内科",
    "advice": "建议您保持规律作息，避免熬夜和过度疲劳，如症状持续或加重，请及时就医。"
  }
}
```

### 4. 医生API

#### 4.1 获取医生资料

- **URL**: `/api/doctor/profile`
- **方法**: GET
- **描述**: 获取当前登录医生的资料
- **请求头**: 需要包含有效的JWT令牌，且用户角色为医生
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "profile": {
      "id": 1,
      "user_id": 2,
      "name": "李医生",
      "gender": "male",
      "title": "主治医师",
      "department": "内科",
      "hospital": "市第一人民医院",
      "license_number": "12345678",
      "specialties": "呼吸系统疾病",
      "introduction": "从事内科临床工作10年，擅长呼吸系统疾病的诊断和治疗。"
    }
  }
}
```

#### 4.2 获取患者列表

- **URL**: `/api/doctor/patients`
- **方法**: GET
- **描述**: 获取医生的患者列表
- **请求头**: 需要包含有效的JWT令牌，且用户角色为医生
- **查询参数**:
  - `page`: 页码，默认为1
  - `limit`: 每页记录数，默认为10
  - `keyword`: 搜索关键词，可搜索患者姓名
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "patients": [
      {
        "id": 1,
        "name": "张三",
        "gender": "male",
        "age": 33,
        "last_consultation": "2023-03-01T14:30:00Z",
        "consultation_count": 2
      },
      {
        "id": 2,
        "name": "李四",
        "gender": "female",
        "age": 28,
        "last_consultation": "2023-03-05T10:15:00Z",
        "consultation_count": 1
      }
    ],
    "pagination": {
      "total": 2,
      "page": 1,
      "limit": 10,
      "pages": 1
    }
  }
}
```

### 5. 管理API

#### 5.1 获取用户列表

- **URL**: `/api/admin/users`
- **方法**: GET
- **描述**: 获取系统用户列表
- **请求头**: 需要包含有效的JWT令牌，且用户角色为管理员
- **查询参数**:
  - `page`: 页码，默认为1
  - `limit`: 每页记录数，默认为10
  - `role`: 用户角色筛选，可选值为`user`、`doctor`、`admin`
  - `status`: 账号状态筛选，可选值为`active`、`inactive`、`banned`
  - `keyword`: 搜索关键词，可搜索用户名、邮箱、手机号
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "users": [
      {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "phone": "13800138000",
        "role": "user",
        "status": "active",
        "created_at": "2023-01-01T12:00:00Z"
      },
      {
        "id": 2,
        "username": "doctor456",
        "email": "doctor@example.com",
        "phone": "13900139000",
        "role": "doctor",
        "status": "active",
        "created_at": "2023-01-02T10:30:00Z"
      }
    ],
    "pagination": {
      "total": 2,
      "page": 1,
      "limit": 10,
      "pages": 1
    }
  }
}
```

#### 5.2 获取症状列表

- **URL**: `/api/admin/symptoms`
- **方法**: GET
- **描述**: 获取系统中的症状列表
- **请求头**: 需要包含有效的JWT令牌，且用户角色为管理员
- **查询参数**:
  - `page`: 页码，默认为1
  - `limit`: 每页记录数，默认为10
  - `body_part`: 身体部位筛选
  - `keyword`: 搜索关键词，可搜索症状名称和描述
- **响应示例**:

```json
{
  "status": "success",
  "data": {
    "symptoms": [
      {
        "id": 1,
        "name": "头痛",
        "description": "头部疼痛感，可能是持续性或间歇性的",
        "body_part": "头部",
        "common_causes": "压力、紧张、疲劳、脱水、偏头痛、鼻窦炎等"
      },
      {
        "id": 2,
        "name": "咳嗽",
        "description": "突然或反复发作的呼吸道清除动作",
        "body_part": "呼吸道",
        "common_causes": "感冒、流感、过敏、哮喘、支气管炎等"
      }
    ],
    "pagination": {
      "total": 2,
      "page": 1,
      "limit": 10,
      "pages": 1
    }
  }
}
```

## 错误码说明

| 错误码 | 描述 |
| ------ | ---- |
| 400 | 请求参数错误 |
| 401 | 未授权或授权失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 409 | 资源冲突 |
| 422 | 请求参数验证失败 |
| 500 | 服务器内部错误 |

## API版本控制

当API发生不兼容的变更时，将通过URL中的版本号进行控制，例如：`/api/v2/symptom/check`。

## 限流策略

为保护系统资源，API实施了限流策略：

- 匿名用户：每IP每分钟最多60次请求
- 已认证用户：每用户每分钟最多120次请求
- 管理员用户：每用户每分钟最多300次请求

超过限制的请求将返回429状态码。

## 最佳实践

1. 始终检查响应中的`status`字段，确保请求成功
2. 实现令牌刷新机制，避免用户会话中断
3. 对敏感数据进行加密传输
4. 实现适当的错误处理和重试机制
5. 缓存不经常变化的数据，减少API调用次数