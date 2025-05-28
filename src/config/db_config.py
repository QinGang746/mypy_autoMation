"""
数据库配置文件
"""
from typing import Dict, Any
import os

# 开发环境数据库配置
DEV_DB_CONFIG = {
    'host': 'easydata-qa1.jd.163.org',
    'user': 'datagather',
    'password': 'datagather',
    'database': 'datagather',
    'port': 3306
}

# 测试环境数据库配置
TEST_DB_CONFIG = {
    'host': 'test-db-server',
    'user': 'test_user',
    'password': 'test_password',
    'database': 'test_db',
    'port': 3306
}

# 生产环境数据库配置
PROD_DB_CONFIG = {
    'host': 'prod-db-server',
    'user': 'prod_user',
    'password': 'prod_password',
    'database': 'prod_db',
    'port': 3306
}

# 配置映射
CONFIG_MAPPING = {
    'development': DEV_DB_CONFIG,
    'testing': TEST_DB_CONFIG,
    'production': PROD_DB_CONFIG
}

def get_db_config(env: str = None) -> Dict[str, Any]:
    """
    获取数据库配置
    
    Args:
        env: 环境名称，可选值为 'development', 'testing', 'production'
             如果未提供，则尝试从环境变量APP_ENV获取，默认为'development'
    
    Returns:
        Dict[str, Any]: 数据库配置字典
    """
    if env is None:
        env = os.environ.get('APP_ENV', 'development')
    
    return CONFIG_MAPPING.get(env, DEV_DB_CONFIG) 