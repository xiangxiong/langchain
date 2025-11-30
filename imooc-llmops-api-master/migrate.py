#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库迁移脚本，用于初始化数据库表结构
"""

import dotenv
from flask import Flask
from flask_migrate import Migrate

from internal.extension.database_extension import db
from internal.extension.migrate_extension import migrate

# 加载环境变量
dotenv.load_dotenv()

# 创建一个简单的Flask应用，仅用于数据库迁移
app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/llmops?client_encoding=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库和迁移
db.init_app(app)
migrate.init_app(app, db, directory="internal/migration")

if __name__ == '__main__':
    # 运行数据库迁移
    with app.app_context():
        # 先启用uuid-ossp扩展
        from sqlalchemy import text
        with db.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            conn.commit()
        
        # 然后运行迁移
        from flask_migrate import upgrade
        upgrade(directory="internal/migration")
        print("数据库迁移完成！")
