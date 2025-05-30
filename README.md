# MySQL数据库Web管理系统
这是一个使用Python Flask和MySQL实现的简单Web数据库管理系统。

## 功能特点
- MySQL数据库连接和操作
- Web界面展示数据库内容
- 支持添加新用户
- 响应式设计，支持移动端访问
- 使用Bootstrap实现美观的UI


## 安装步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
# 或者是
python -m pip install -r requirements.txt
```

2. 配置环境变量：
创建`.env`文件并设置以下变量：
- MYSQL_HOST
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_DATABASE
- MYSQL_PORT
- MYSQL_TABLE

3. 运行应用：
```bash
python app.py
```

4. 访问应用：
打开浏览器访问 http://localhost:5000

## 技术栈
- Python Flask
- PyMySQL
- Flask-Bootstrap
- HTML/CSS/JavaScript 