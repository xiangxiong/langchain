#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建测试账号脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from flask import Flask
from internal.model.account import Account
from pkg.sqlalchemy import SQLAlchemy
from pkg.password import hash_password
import secrets
import base64

# 加载环境变量
load_dotenv()

# 创建Flask应用实例
app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/llmops?client_encoding=utf8')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
from internal.extension.database_extension import db
db.init_app(app)

# 创建测试账号
def create_test_account():
    with app.app_context():
        # 检查账号是否已存在
        email = 'zhangsan@example.com'
        existing_account = Account.query.filter_by(email=email).first()
        if existing_account:
            print(f"账号 {email} 已存在")
            return
        
        # 生成密码盐值
        salt = secrets.token_bytes(16)
        base64_salt = base64.b64encode(salt).decode()
        
        # 密码哈希
        password = 'zhangsan1@example.com'
        password_hashed = hash_password(password, salt)
        base64_password_hashed = base64.b64encode(password_hashed).decode()
        
        # 创建账号
        account = Account(
            name='张三',
            email=email,
            password=base64_password_hashed,
            password_salt=base64_salt
        )
        
        db.session.add(account)
        db.session.commit()
        
        print(f"测试账号创建成功！")
        print(f"邮箱: {email}")
        print(f"密码: {password}")

if __name__ == '__main__':
    create_test_account()
