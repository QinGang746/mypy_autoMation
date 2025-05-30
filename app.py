from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import pymysql
import os
from dotenv import load_dotenv
import hashlib

# 加载环境变量
load_dotenv()
app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 用于flash消息
Bootstrap(app)


# 数据库配置
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': int(os.getenv('MYSQL_PORT')),
}

def get_db_connection():
    """
    创建并返回数据库连接
    返回: MySQL数据库连接对象
    """
    return pymysql.connect(**db_config)

def hash_password(password):
    """
    使用SHA256算法对密码进行加密
    参数:
        password: 原始密码
    返回:
        加密后的密码哈希值
    """
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    """
    主页路由
    功能：
    1. 从数据库获取所有用户信息
    2. 格式化日期时间
    3. 渲染主页模板
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # 获取表中的所有数据
        table_name = os.getenv('MYSQL_TABLE')
        cursor.execute(f"""
            SELECT user_id, username, email, age, 
                   created_at, updated_at, is_active 
            FROM {table_name}
            ORDER BY created_at DESC
        """)
        data = cursor.fetchall()
        
        # 格式化日期时间
        for row in data:
            if row['created_at']:
                row['created_at'] = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if row['updated_at']:
                row['updated_at'] = row['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.close()
        conn.close()
        return render_template('index.html', data=data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    """
    添加新用户的路由
    功能：
    1. 接收并验证用户提交的表单数据
    2. 对密码进行加密
    3. 将新用户数据插入数据库
    4. 处理可能的错误（如用户名或邮箱重复）
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        
        # 验证必填字段
        if not all([username, email, password]):
            return jsonify({'error': '用户名、邮箱和密码为必填项'}), 400
        
        # 密码加密
        password_hash = hash_password(password)
        
        table_name = os.getenv('MYSQL_TABLE')
        
        # 插入新用户
        sql = f"""
            INSERT INTO {table_name} 
            (username, email, password_hash, age) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (username, email, password_hash, age or None))
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({'message': '用户添加成功'}), 200
    except pymysql.err.IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'error': '用户名已存在'}), 400
        elif 'email' in str(e):
            return jsonify({'error': '邮箱已存在'}), 400
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/toggle_active/<int:user_id>', methods=['POST'])
def toggle_active(user_id):
    """
    切换用户激活状态的路由
    功能：
    1. 接收用户ID
    2. 在数据库中切换该用户的激活状态（激活/禁用）
    参数:
        user_id: 要切换状态的用户ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        table_name = os.getenv('MYSQL_TABLE')
        
        # 切换用户激活状态
        cursor.execute(f"""
            UPDATE {table_name} 
            SET is_active = NOT is_active 
            WHERE user_id = %s
        """, (user_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({'message': '状态更新成功'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 