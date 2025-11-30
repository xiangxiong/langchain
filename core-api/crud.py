from database import User, get_db


# 创建用户
def create_user(userName: str, passWord: str, sex: str):
    db_generator = get_db()
    db = next(db_generator)
    try:
        db_user = User(userName=userName, passWord=passWord, sex=sex)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        next(db_generator, None)  # 关闭生成器


# 根据ID获取用户
def get_user(user_id: int):
    db_generator = get_db()
    db = next(db_generator)
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    finally:
        next(db_generator, None)  # 关闭生成器


# 获取所有用户
def get_users(skip: int = 0, limit: int = 100):
    db_generator = get_db()
    db = next(db_generator)
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    finally:
        next(db_generator, None)  # 关闭生成器


# 更新用户信息
def update_user(user_id: int, userName: str = None, passWord: str = None, sex: str = None):
    db_generator = get_db()
    db = next(db_generator)
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            if userName is not None:
                db_user.userName = userName
            if passWord is not None:
                db_user.passWord = passWord
            if sex is not None:
                db_user.sex = sex
            db.commit()
            db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        next(db_generator, None)  # 关闭生成器


# 删除用户
def delete_user(user_id: int):
    db_generator = get_db()
    db = next(db_generator)
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e
    finally:
        next(db_generator, None)  # 关闭生成器