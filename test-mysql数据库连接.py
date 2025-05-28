"""
MySQL数据库连接测试模块
"""
import logging
import os
from src.config.db_config import get_db_config
from src.database.connection import DatabaseConnection
from src.database.mysql_operations import MySQLOperations


def main():
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 获取数据库配置
    db_config = get_db_config()
    
    # 创建数据库连接管理器
    db_connection = DatabaseConnection(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port']
    )
    
    try:
        # 使用上下文管理器自动处理连接的建立和关闭
        with db_connection as connection:
            # 创建MySQL操作对象
            mysql_ops = MySQLOperations(connection)
            
            # 执行查询并获取第一行数据
            mysql_ops.execute_query("SELECT * FROM qgtest_user")
            first_row = mysql_ops.fetch_one()
            print("\n第一行数据:", first_row)
            print("数据类型:", type(first_row))
            
            # 重新执行查询并获取所有数据
            mysql_ops.execute_query("SELECT * FROM qgtest_user")
            all_rows = mysql_ops.fetch_all()
            print("\n所有数据:", all_rows)
            print("数据类型:", type(all_rows))
            
    except Exception as e:
        logging.error(f"程序执行出错: {str(e)}")


if __name__ == "__main__":
    main()
