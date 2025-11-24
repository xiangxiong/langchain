# app.py
from flask import Flask

# 创建 Flask 应用实例
app = Flask(__name__)

# 定义路由和视图函数
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/name')
def get_name():
    return f'Hello, nem!'

# 如果直接运行此脚本，则启动开发服务器
if __name__ == '__main__':
    app.run(debug=True)
