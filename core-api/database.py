from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库配置
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/llmops"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建基类
Base = declarative_base()

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String, index=True, nullable=False)
    passWord = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "userName": self.userName,
            "passWord": self.passWord,
            "sex": self.sex
        }


# 创建所有表
def init_db():
    Base.metadata.create_all(bind=engine)


# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 在应用启动时初始化数据库
def init_app(app: Flask):
    with app.app_context():
        init_db()