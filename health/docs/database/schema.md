# 智医通数据库设计

## 数据库概述

智医通系统采用关系型数据库MySQL作为主要数据存储，同时使用MongoDB存储非结构化的医疗数据。数据库设计遵循第三范式，确保数据的一致性和完整性。

## 数据库表设计

### 用户相关表

#### 用户表 (users)

存储系统所有用户的基本信息。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 用户ID |
| username | VARCHAR(50) | NOT NULL, UNIQUE | 用户名 |
| password | VARCHAR(255) | NOT NULL | 密码（加密存储） |
| email | VARCHAR(100) | NOT NULL, UNIQUE | 邮箱 |
| phone | VARCHAR(20) | UNIQUE | 手机号 |
| role | ENUM('user', 'doctor', 'admin') | NOT NULL, DEFAULT 'user' | 用户角色 |
| status | ENUM('active', 'inactive', 'banned') | NOT NULL, DEFAULT 'active' | 账号状态 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 患者信息表 (patient_profiles)

存储患者的详细个人信息和健康档案。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 档案ID |
| user_id | INT | NOT NULL, FOREIGN KEY | 关联用户ID |
| name | VARCHAR(50) | NOT NULL | 姓名 |
| gender | ENUM('male', 'female', 'other') | NOT NULL | 性别 |
| birth_date | DATE | NOT NULL | 出生日期 |
| height | DECIMAL(5,2) | | 身高(cm) |
| weight | DECIMAL(5,2) | | 体重(kg) |
| blood_type | ENUM('A', 'B', 'AB', 'O', 'unknown') | DEFAULT 'unknown' | 血型 |
| allergies | TEXT | | 过敏史 |
| chronic_diseases | TEXT | | 慢性病史 |
| family_history | TEXT | | 家族病史 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 医生信息表 (doctor_profiles)

存储医生的专业信息和资质。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 档案ID |
| user_id | INT | NOT NULL, FOREIGN KEY | 关联用户ID |
| name | VARCHAR(50) | NOT NULL | 姓名 |
| gender | ENUM('male', 'female', 'other') | NOT NULL | 性别 |
| title | VARCHAR(50) | NOT NULL | 职称 |
| department | VARCHAR(50) | NOT NULL | 科室 |
| hospital | VARCHAR(100) | NOT NULL | 医院 |
| license_number | VARCHAR(50) | NOT NULL, UNIQUE | 执业证号 |
| specialties | TEXT | | 专长 |
| introduction | TEXT | | 简介 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

### 医疗知识库相关表

#### 症状表 (symptoms)

存储系统中所有症状的详细信息。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 症状ID |
| name | VARCHAR(100) | NOT NULL, UNIQUE | 症状名称 |
| description | TEXT | NOT NULL | 描述 |
| keywords | TEXT | | 关键词（用于搜索） |
| body_part | VARCHAR(50) | | 身体部位 |
| severity_levels | JSON | | 严重程度级别 |
| common_causes | TEXT | | 常见原因 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 症状同义词表 (symptom_synonyms)

存储症状的同义词，用于自然语言处理。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | ID |
| symptom_id | INT | NOT NULL, FOREIGN KEY | 关联症状ID |
| synonym | VARCHAR(100) | NOT NULL | 同义词 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 疾病表 (diseases)

存储系统中所有疾病的详细信息。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 疾病ID |
| name | VARCHAR(100) | NOT NULL, UNIQUE | 疾病名称 |
| icd_code | VARCHAR(20) | UNIQUE | ICD-10编码 |
| description | TEXT | NOT NULL | 描述 |
| risk_factors | TEXT | | 风险因素 |
| prevention | TEXT | | 预防措施 |
| treatment | TEXT | | 治疗方法 |
| department | VARCHAR(50) | NOT NULL | 就诊科室 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 疾病症状关联表 (disease_symptoms)

存储疾病和症状之间的多对多关系。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | ID |
| disease_id | INT | NOT NULL, FOREIGN KEY | 疾病ID |
| symptom_id | INT | NOT NULL, FOREIGN KEY | 症状ID |
| relevance | DECIMAL(3,2) | NOT NULL, DEFAULT 0.5 | 相关性（0-1） |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 问诊相关表

#### 问诊记录表 (consultations)

存储用户的问诊记录。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 问诊ID |
| patient_id | INT | NOT NULL, FOREIGN KEY | 患者ID |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| chief_complaint | TEXT | NOT NULL | 主诉 |
| symptom_description | TEXT | | 症状描述 |
| duration | VARCHAR(50) | | 持续时间 |
| severity | ENUM('mild', 'moderate', 'severe') | | 严重程度 |
| status | ENUM('in_progress', 'completed', 'cancelled') | NOT NULL, DEFAULT 'in_progress' | 状态 |
| completed_at | TIMESTAMP | | 完成时间 |

#### 问诊问答表 (consultation_qa)

存储问诊过程中的问答记录。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | ID |
| consultation_id | INT | NOT NULL, FOREIGN KEY | 问诊ID |
| question | TEXT | NOT NULL | 问题 |
| answer | TEXT | | 回答 |
| sequence | INT | NOT NULL | 序号 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 诊断结果表 (diagnoses)

存储问诊的诊断结果。

| 字段名 | 类型 | 约束 | 说明 |
| ------ | ---- | ---- | ---- |
| id | INT | PRIMARY KEY, AUTO_INCREMENT | ID |
| consultation_id | INT | NOT NULL, FOREIGN KEY, UNIQUE | 问诊ID |
| possible_diseases | JSON | NOT NULL | 可能疾病（JSON格式，包含疾病ID和概率） |
| risk_level | ENUM('low', 'medium', 'high') | NOT NULL | 风险等级 |
| recommended_department | VARCHAR(50) | NOT NULL | 推荐科室 |
| advice | TEXT | | 建议 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

## 数据库索引

为提高查询性能，系统将在以下字段上创建索引：

1. users表：username, email, phone, role
2. patient_profiles表：user_id, name
3. doctor_profiles表：user_id, name, department, hospital, license_number
4. symptoms表：name, body_part
5. diseases表：name, icd_code, department
6. consultations表：patient_id, status, created_at
7. diagnoses表：consultation_id, risk_level, recommended_department

## 数据库关系图

```
+---------------+       +-------------------+       +------------------+
|     users     |       | patient_profiles  |       | doctor_profiles  |
+---------------+       +-------------------+       +------------------+
| id            |<----->| user_id          |       | user_id          |
| username      |       | name             |       | name             |
| password      |       | gender           |       | gender           |
| email         |       | birth_date       |       | title            |
| phone         |       | ...              |       | ...              |
| role          |<----->+-------------------+       +------------------+
| ...           |
+---------------+
       ^
       |
       v
+---------------+       +-------------------+       +------------------+
| consultations |       | consultation_qa   |       |    diagnoses     |
+---------------+       +-------------------+       +------------------+
| id            |<----->| consultation_id   |<----->| consultation_id  |
| patient_id    |       | question          |       | possible_diseases|
| chief_complaint|       | answer           |       | risk_level       |
| ...           |       | ...              |       | ...              |
+---------------+       +-------------------+       +------------------+
       ^
       |
       v
+---------------+       +-------------------+       +------------------+
|   symptoms    |<----->| disease_symptoms  |<----->|    diseases      |
+---------------+       +-------------------+       +------------------+
| id            |       | disease_id        |       | id               |
| name          |       | symptom_id        |       | name             |
| description   |       | relevance         |       | icd_code         |
| ...           |       | ...              |       | ...              |
+---------------+       +-------------------+       +------------------+
       ^
       |
       v
+------------------+
| symptom_synonyms |
+------------------+
| id               |
| symptom_id       |
| synonym          |
| ...              |
+------------------+
```

## 数据库迁移策略

系统将使用Alembic作为数据库迁移工具，确保数据库结构的版本控制和平滑升级。迁移脚本将存放在`backend/migrations`目录中。

## 数据安全策略

1. 用户密码使用bcrypt算法加密存储
2. 敏感个人信息（如病史）进行加密存储
3. 数据库定期备份
4. 实施行级权限控制，确保用户只能访问自己的数据
5. 所有数据库操作记录日志，便于审计

## 性能优化策略

1. 对频繁查询的表进行适当的分区
2. 使用连接池管理数据库连接
3. 对大型表实施分表策略
4. 定期进行数据库维护和优化
5. 实施查询缓存机制，减少数据库负载