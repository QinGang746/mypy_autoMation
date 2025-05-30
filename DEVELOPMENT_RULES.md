# 用户管理系统开发规范

## 1. 项目结构规范

```
project_root/
├── app.py                 # 主应用程序入口
├── templates/             # HTML模板文件
│   └── *.html
├── static/               # 静态资源文件
│   ├── css/
│   ├── js/
│   └── img/
├── .env                  # 环境变量配置
└── requirements.txt      # 项目依赖
```

## 2. 代码风格规范

### 2.1 Python代码规范

- 遵循PEP 8规范
- 缩进使用4个空格
- 文件编码统一使用UTF-8
- 每个函数必须包含文档字符串，说明功能、参数和返回值
- 变量命名采用小写字母加下划线
- 类名采用驼峰命名法
- 常量使用大写字母加下划线

示例：
```python
def get_user_info(user_id):
    """
    获取用户信息
    参数:
        user_id: 用户ID
    返回:
        用户信息字典
    """
    pass
```

### 2.2 HTML模板规范

- 使用4个空格缩进
- 标签属性使用双引号
- 模板文件必须继承基础模板
- 块名称使用小写字母加下划线
- 保持HTML结构清晰，适当添加注释

示例：
```html
{% extends "base.html" %}
{% block content %}
    <!-- 用户信息表单 -->
    <div class="user-form">
        ...
    </div>
{% endblock %}
```

### 2.3 JavaScript规范

- 使用ES6+语法
- 使用4个空格缩进
- 变量声明使用const和let
- 函数名使用驼峰命名法
- 异步操作使用async/await或Promise
- 适当添加错误处理

示例：
```javascript
async function getUserData(userId) {
    try {
        const response = await fetch(`/api/user/${userId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('获取用户数据失败:', error);
        throw error;
    }
}
```

## 3. 数据库规范

### 3.1 表命名规范

- 表名使用小写字母加下划线
- 主键统一命名为`id`或`表名_id`
- 外键命名格式：`关联表名_id`
- 时间戳字段：`created_at`、`updated_at`
- 状态字段：`is_状态名`（如：is_active）

### 3.2 字段规范

- 字段名使用小写字母加下划线
- 必须指定字段类型和长度
- 所有表必须包含created_at和updated_at
- 敏感数据必须加密存储
- 适当使用索引优化查询

## 4. API规范

### 4.1 接口命名

- 使用RESTful风格
- URL使用小写字母加下划线或中划线
- 使用名词表示资源，动词表示操作

示例：
```
GET    /api/users         # 获取用户列表
POST   /api/users         # 创建用户
PUT    /api/users/{id}    # 更新用户
DELETE /api/users/{id}    # 删除用户
```

### 4.2 响应格式

```json
{
    "code": 200,          // 状态码
    "message": "成功",    // 响应消息
    "data": {            // 响应数据
        ...
    }
}
```

## 5. 安全规范

### 5.1 数据安全

- 密码必须加密存储（使用SHA256）
- 敏感配置使用环境变量
- API接口需要进行权限验证
- 防止SQL注入，使用参数化查询
- 定期备份数据库

### 5.2 输入验证

- 所有用户输入必须验证
- 特殊字符需要转义
- 文件上传需要验证类型和大小
- 防止XSS攻击

## 6. 错误处理规范

### 6.1 后端错误处理

- 使用try-except捕获异常
- 记录详细错误日志
- 返回合适的HTTP状态码
- 提供友好的错误提示

### 6.2 前端错误处理

- 表单验证提供即时反馈
- AJAX请求错误统一处理
- 显示用户友好的错误消息
- 保持用户数据，避免重复输入

## 7. 版本控制规范

### 7.1 Git使用规范

- 主分支：master/main
- 开发分支：develop
- 功能分支：feature/功能名
- 修复分支：hotfix/问题描述

### 7.2 提交信息规范

```
类型(范围): 简短描述

详细描述
```

类型包括：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 8. 测试规范

### 8.1 单元测试

- 每个功能模块必须编写测试用例
- 测试覆盖率要求达到80%以上
- 测试用例命名清晰明确
- 保持测试用例的独立性

### 8.2 集成测试

- 主要功能流程测试
- 数据库操作测试
- API接口测试
- 浏览器兼容性测试

## 9. 文档规范

### 9.1 代码注释

- 复杂逻辑必须添加注释
- 公共函数必须有文档字符串
- 注释要简洁清晰
- 及时更新注释

### 9.2 项目文档

- README.md：项目说明
- CHANGELOG.md：版本更新记录
- API文档：接口说明
- 部署文档：部署步骤

## 10. 性能规范

### 10.1 后端性能

- 使用连接池管理数据库连接
- 合理使用缓存
- 优化SQL查询
- 控制响应时间在500ms以内

### 10.2 前端性能

- 压缩静态资源
- 使用CDN加速
- 减少HTTP请求
- 优化JavaScript代码执行效率 