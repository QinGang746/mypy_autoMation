from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import pymysql
import os
from dotenv import load_dotenv
import hashlib

# 加载环境变量
load_dotenv()

# Flask应用初始化
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')  # 从环境变量获取密钥
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
    """创建并返回数据库连接"""
    return pymysql.connect(**db_config)

def hash_password(password):
    """使用SHA256算法对密码进行加密
    
    Args:
        password (str): 原始密码
        
    Returns:
        str: 加密后的密码哈希值
    """
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    """主页路由 - 显示所有用户信息"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
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
    """添加新用户的路由
    
    功能：
    1. 接收并验证用户提交的表单数据
    2. 对密码进行加密
    3. 将新用户数据插入数据库
    4. 处理可能的错误（如用户名或邮箱重复）
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取并验证表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        
        if not all([username, email, password]):
            return jsonify({'error': '用户名、邮箱和密码为必填项'}), 400
        
        # 密码加密并插入数据
        password_hash = hash_password(password)
        table_name = os.getenv('MYSQL_TABLE')
        
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
    """切换用户激活状态的路由
    
    Args:
        user_id (int): 要切换状态的用户ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        table_name = os.getenv('MYSQL_TABLE')
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

@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取单个用户信息的路由
    
    Args:
        user_id (int): 要获取的用户ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        table_name = os.getenv('MYSQL_TABLE')
        cursor.execute(f"""
            SELECT user_id, username, email, age, is_active 
            FROM {table_name} 
            WHERE user_id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return jsonify(user), 200
        return jsonify({'error': '用户不存在'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    """编辑用户信息的路由
    Args:
        user_id (int): 要编辑的用户ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取并验证表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        age = request.form.get('age')
        password = request.form.get('password')
        is_active = request.form.get('is_active')
        
        if not all([username, email]):
            return jsonify({'error': '用户名和邮箱为必填项'}), 400
            
        # 准备更新字段
        update_fields = []
        params = []
        
        update_fields.extend([
            "username = %s",
            "email = %s",
            "age = %s"
        ])
        params.extend([username, email, age if age else None])
        
        if password:
            update_fields.append("password_hash = %s")
            params.append(hash_password(password))
            
        if is_active is not None:
            update_fields.append("is_active = %s")
            params.append(is_active == 'true')
            
        params.append(user_id)
        
        # 执行更新
        table_name = os.getenv('MYSQL_TABLE')
        sql = f"""
            UPDATE {table_name} 
            SET {', '.join(update_fields)}
            WHERE user_id = %s
        """
        
        cursor.execute(sql, tuple(params))
        conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({'message': '用户信息更新成功'}), 200
        
    except pymysql.err.IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'error': '用户名已存在'}), 400
        elif 'email' in str(e):
            return jsonify({'error': '邮箱已存在'}), 400
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """删除用户的路由
    
    Args:
        user_id (int): 要删除的用户ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        table_name = os.getenv('MYSQL_TABLE')
        cursor.execute(f"""
            DELETE FROM {table_name} 
            WHERE user_id = %s
        """, (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': '用户删除成功'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)