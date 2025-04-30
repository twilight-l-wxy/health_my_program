# 智医通项目部署指南

本文档提供了智医通项目的完整部署流程，包括开发环境配置、数据库设置、前后端部署以及AI模型部署。

## 1. 环境要求

### 系统要求
- 操作系统：Windows/Linux/MacOS
- CPU：至少4核
- 内存：至少8GB（推荐16GB以上）
- 存储：至少20GB可用空间
- GPU：用于AI模型训练和推理（可选，但推荐）

### 软件要求
- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- MongoDB 4.4+（可选，用于存储非结构化数据）
- Git

## 2. 开发环境配置

### 2.1 克隆代码仓库

```bash
# 克隆代码仓库
# 注意：目前项目尚未上传到GitHub，以下为示例命令，实际URL请以最终发布的仓库地址为准
git clone https://github.com/your-username/zhiyitong.git
cd zhiyitong
```

### 2.2 配置前端环境

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端开发服务器将在 http://localhost:3000 启动。

### 2.3 配置后端环境

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# Windows
copy .env.example .env
# Linux/MacOS
cp .env.example .env

# 编辑.env文件，设置数据库连接等配置

# 启动开发服务器
python app.py
```

后端API服务将在 http://localhost:5000 启动。

### 2.4 配置AI模型环境

```bash
# 进入AI模型目录
cd ai_model

# 安装依赖（确保已激活虚拟环境）
pip install -r requirements.txt

# 下载预训练模型（示例）
python download_models.py
```

## 3. 数据库设置

### 3.1 MySQL数据库

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE zhiyitong CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户并授权
CREATE USER 'zhiyitong_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON zhiyitong.* TO 'zhiyitong_user'@'localhost';
FLUSH PRIVILEGES;

# 退出MySQL
EXIT;
```

### 3.2 初始化数据库

```bash
# 进入后端目录
cd backend

# 确保已激活虚拟环境

# 初始化数据库迁移
python -c "from app import db; db.create_all()"

# 导入初始数据
python scripts/import_initial_data.py
```

## 4. 生产环境部署

### 4.1 前端部署

```bash
# 进入前端目录
cd frontend

# 构建生产版本
npm run build

# 生成的静态文件位于dist目录中，可以部署到Nginx或其他Web服务器
```

#### Nginx配置示例

```nginx
server {
    listen 80;
    server_name zhiyitong.example.com;

    root /path/to/zhiyitong/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4.2 后端部署

```bash
# 进入后端目录
cd backend

# 安装Gunicorn
pip install gunicorn

# 启动Gunicorn服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Systemd服务配置示例

创建文件 `/etc/systemd/system/zhiyitong.service`：

```ini
[Unit]
Description=Zhiyitong Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/zhiyitong/backend
Environment="PATH=/path/to/zhiyitong/backend/venv/bin"
ExecStart=/path/to/zhiyitong/backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable zhiyitong
sudo systemctl start zhiyitong
```

### 4.3 AI模型部署

对于轻量级部署，可以将AI模型集成到后端服务中。对于更大规模的部署，建议使用单独的服务：

```bash
# 进入AI模型目录
cd ai_model

# 启动模型服务
python model_server.py
```

#### 使用ONNX Runtime优化模型

```bash
# 转换模型为ONNX格式
python scripts/convert_to_onnx.py

# 量化模型
python scripts/quantize_model.py
```

## 5. 监控与维护

### 5.1 日志管理

日志文件位于：
- 前端：Nginx日志目录
- 后端：`/path/to/zhiyitong/backend/logs/`
- AI模型：`/path/to/zhiyitong/ai_model/logs/`

### 5.2 数据库备份

```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATETIME=$(date +"%Y%m%d_%H%M%S")
MYSQL_USER="zhiyitong_user"
MYSQL_PASSWORD="your_password"
DATABASE_NAME="zhiyitong"

mkdir -p $BACKUP_DIR

# 备份MySQL数据库
mysqldump -u $MYSQL_USER -p$MYSQL_PASSWORD $DATABASE_NAME > $BACKUP_DIR/zhiyitong_$DATETIME.sql

# 压缩备份文件
gzip $BACKUP_DIR/zhiyitong_$DATETIME.sql

# 删除30天前的备份
find $BACKUP_DIR -name "zhiyitong_*.sql.gz" -type f -mtime +30 -delete
EOF

# 添加执行权限
chmod +x backup.sh

# 添加到crontab，每天凌晨3点执行
(crontab -l 2>/dev/null; echo "0 3 * * * /path/to/backup.sh") | crontab -
```

## 6. 扩展与优化

### 6.1 负载均衡

对于高流量场景，可以使用Nginx进行负载均衡：

```nginx
upstream backend {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 80;
    server_name api.zhiyitong.example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 6.2 缓存策略

- 前端：使用浏览器缓存和CDN
- 后端：使用Redis缓存频繁访问的数据
- 数据库：优化查询和索引

### 6.3 安全措施

- 启用HTTPS
- 实施CSRF保护
- 设置适当的CORS策略
- 定期更新依赖包
- 实施API限流
- 加密敏感数据

## 7. 常见问题解决

### 7.1 前端构建失败

- 检查Node.js版本是否兼容
- 删除node_modules目录并重新安装依赖
- 检查package.json中的依赖版本

### 7.2 后端启动失败

- 检查数据库连接配置
- 确保所有依赖已正确安装
- 检查日志文件获取详细错误信息

### 7.3 AI模型加载错误

- 确保模型文件已正确下载
- 检查GPU驱动和CUDA版本兼容性
- 尝试使用CPU模式运行

## 8. 联系与支持

如有任何部署问题，请联系项目维护团队：

- 邮箱：support@zhiyitong.example.com
- 问题追踪：https://github.com/your-username/zhiyitong/issues

**注意**：目前项目尚未正式上传到GitHub，上述GitHub链接为示例。项目正式发布后，将更新为实际的仓库地址。

---

本部署指南最后更新于：2024年4月