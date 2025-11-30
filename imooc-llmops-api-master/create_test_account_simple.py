#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单创建测试账号脚本
"""
import os
import sys
import uuid
import secrets
import base64
import hashlib
from datetime import datetime

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 密码哈希函数
def hash_password(password: str, salt: bytes) -> bytes:
    """将传入的密码+盐值进行哈希加密"""
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)
    return dk

# 简单的数据库连接和操作
from sqlalchemy import create_engine, Column, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 获取数据库连接URL
db_url = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/llmops?client_encoding=utf8')

# 创建数据库引擎
engine = create_engine(db_url)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 定义Account模型
class Account(Base):
    __tablename__ = "account"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, server_default=text("''::character varying"))
    email = Column(String(255), nullable=False, server_default=text("''::character varying"))
    avatar = Column(String(255), nullable=False, server_default=text("''::character varying"))
    password = Column(String(255), nullable=True, server_default=text("''::character varying"))
    password_salt = Column(String(255), nullable=True, server_default=text("''::character varying"))
    assistant_agent_conversation_id = Column(String, nullable=True)
    last_login_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP(0)"))
    last_login_ip = Column(String(255), nullable=False, server_default=text("''::character varying"))
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(0)"),
        onupdate=datetime.now
    )
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP(0)"))

# 创建测试账号
def create_test_account():
    # 创建会话
    db = SessionLocal()
    
    try:
        # 检查账号是否已存在
        email = 'zhangsan@example.com'
        existing_account = db.query(Account).filter(Account.email == email).first()
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
        
        db.add(account)
        db.commit()
        
        print(f"测试账号创建成功！")
        print(f"邮箱: {email}")
        print(f"密码: {password}")
    finally:
        # 关闭会话
        db.close()

if __name__ == '__main__':
    create_test_account()
