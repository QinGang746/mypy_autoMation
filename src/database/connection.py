"""
数据库连接管理模块
"""
from typing import Optional
import logging
import pymysql
from pymysql.connections import Connection


class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        """
        初始化数据库连接管理器
        
        Args:
            host: 数据库主机地址
            user: 用户名
            password: 密码
            database: 数据库名
            port: 端口号（默认3306）
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection: Optional[Connection] = None
        
    def connect(self) -> Connection:
        """
        建立数据库连接
        
        Returns:
            Connection: MySQL连接对象
        """
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            logging.info("数据库连接成功")
            return self.connection
        except Exception as e:
            logging.error(f"数据库连接失败: {str(e)}")
            raise
            
    def close(self) -> None:
        """关闭数据库连接"""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
            logging.info("数据库连接已关闭")
        except Exception as e:
            logging.error(f"关闭数据库连接失败: {str(e)}")
            raise
            
    def __enter__(self) -> Connection:
        """上下文管理器入口"""
        return self.connect()
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器出口"""
        self.close() 