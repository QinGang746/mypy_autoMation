# 数据库连接配置项目

## 项目结构

```
项目根目录/
├── src/                      # 源代码目录
│   ├── core/                 # 核心功能
│   │   ├── config/           # 配置文件
│   │   │   ├── __init__.py
│   │   │   └── db_config.py  # 数据库配置
│   │   
│   └── __init__.py
├── .env                      # 环境变量文件
├── test-mysql数据库连接.py    # 测试脚本
└── README.md                 # 项目说明
```

## 使用说明

### 数据库配置

数据库配置已经从主代码中分离出来，存放在 `src/core/config/db_config.py` 文件中。这个文件定义了不同环境（开发、测试、生产）的数据库连接参数。

### 如何选择环境

可以通过以下几种方式选择使用哪个环境的配置：

1. 设置环境变量：
   ```python
   import os
   os.environ['APP_ENV'] = 'development'  # 或 'testing', 'production'
   ```

2. 直接在函数调用时指定：
   ```python
   db_manager = create_db_manager_from_config('development')
   ```

3. 通过 `.env` 文件设置（需要安装 python-dotenv 包）：
   ```
   APP_ENV=development
   ```

### 运行测试脚本

```bash
python test-mysql数据库连接.py
```

## 配置自定义环境

如需添加新的环境配置，请编辑 `src/core/config/db_config.py` 文件，添加新的配置字典并更新 `CONFIG_MAPPING`。 
