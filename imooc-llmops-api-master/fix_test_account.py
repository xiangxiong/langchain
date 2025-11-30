#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复测试账号密码脚本
"""
import os
import sys
import uuid
import secrets
import base64
import hashlib
import binascii
from datetime import datetime

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 系统实际使用的密码哈希函数
def hash_password(password: str, salt: bytes) -> bytes:
    """将传入的密码+盐值进行哈希加密"""
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)
    return binascii.hexlify(dk)  # 注意这里使用了binascii.hexlify

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

# 修复测试账号密码
def fix_test_account_password():
    # 创建会话
    db = SessionLocal()
    
    try:
        # 查找账号
        email = 'zhangsan@example.com'
        account = db.query(Account).filter(Account.email == email).first()
        if not account:
            print(f"账号 {email} 不存在")
            return
        
        # 生成正确的密码盐值和哈希
        password = 'zhangsan1@example.com'
        
        # 1.生成密码随机盐值
        salt = secrets.token_bytes(16)
        base64_salt = base64.b64encode(salt).decode()
        
        # 2.利用盐值和password进行加密
        password_hashed = hash_password(password, salt)
        base64_password_hashed = base64.b64encode(password_hashed).decode()
        
        # 更新账号密码
        account.password = base64_password_hashed
        account.password_salt = base64_salt
        
        db.commit()
        
        print(f"测试账号密码修复成功！")
        print(f"邮箱: {email}")
        print(f"密码: {password}")
    finally:
        # 关闭会话
        db.close()

if __name__ == '__main__':
    fix_test_account_password()
