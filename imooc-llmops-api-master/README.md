# LLMOps API 接口文档

# AI 应用模块
* Python 3.8+
* Postgres 15+
* Redis 7+
* LangChain 0.0.27.

## 快速开始 (Quick Start)

### 1. 环境准备
确保你已经安装了 Python 3.8+ 和 Docker。

### 2. 启动基础服务 (Docker)
本项目依赖 PostgreSQL 和 Redis，请使用 Docker Compose 启动：
```bash
docker-compose up -d
```

### 3. Python 环境配置
建议使用虚拟环境：
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境 (Mac/Linux)
source venv/bin/activate

# 激活虚拟环境 (Windows)
# venv\Scripts\activate
```

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 配置文件
复制示例配置文件并修改：
```bash
cp .env.example .env
```
**注意**：如果你是在本地运行 Flask 应用，请确保 `.env` 中的数据库和 Redis 连接地址指向 `localhost`：
```ini
# .env 修改示例
SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/llmops?client_encoding=utf8
REDIS_HOST=localhost
```

### 6. 数据库迁移
初始化数据库表结构：
```bash
export FLASK_APP=app/http/app.py
flask db upgrade
```

### 7. 运行应用
```bash
python app/http/app.py
```
应用将运行在 `http://127.0.0.1:5000`。

---

## 常用服务访问
*   **API 服务**: `http://localhost:5000`
*   **pgAdmin (数据库管理)**: `http://localhost:5050`
    *   账号: `admin@example.com`
    *   密码: `admin`
*   **PostgreSQL**: `localhost:5432`
*   **Redis**: `localhost:6379`
