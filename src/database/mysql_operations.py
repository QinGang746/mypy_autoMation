"""
MySQL数据库操作公共方法模块
"""
from typing import List, Tuple, Optional, Any, Dict
import logging
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor


class MySQLOperations:
    def __init__(self, connection: Connection):
        """
        初始化MySQL操作类
        
        Args:
            connection: MySQL数据库连接对象
        """
        self.connection = connection
        self.cursor: Optional[Cursor] = None
        
    def _ensure_cursor(self) -> None:
        """确保游标已创建"""
        if self.cursor is None:
            self.cursor = self.connection.cursor()
            
    def execute_query(self, query: str, params: tuple = None) -> None:
        """
        执行SQL查询
        
        Args:
            query: SQL查询语句
            params: 查询参数元组（可选）
        """
        try:
            self._ensure_cursor()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            logging.info(f"SQL查询执行成功: {query}")
        except Exception as e:
            logging.error(f"SQL查询执行失败: {str(e)}")
            raise
            
    def fetch_one(self) -> Optional[Tuple]:
        """
        获取查询结果的第一行
        
        Returns:
            Optional[Tuple]: 查询结果的第一行，如果没有结果则返回None
        """
        try:
            self._ensure_cursor()
            result = self.cursor.fetchone()
            logging.info("成功获取第一行数据")
            return result
        except Exception as e:
            logging.error(f"获取第一行数据失败: {str(e)}")
            raise
            
    def fetch_all(self) -> List[Tuple]:
        """
        获取查询结果的所有行
        
        Returns:
            List[Tuple]: 查询结果的所有行
        """
        try:
            self._ensure_cursor()
            result = self.cursor.fetchall()
            logging.info("成功获取所有数据")
            return result
        except Exception as e:
            logging.error(f"获取所有数据失败: {str(e)}")
            raise
            
    def execute_insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        执行插入操作
        
        Args:
            table: 表名
            data: 要插入的数据字典，键为列名，值为列值
            
        Returns:
            int: 插入的记录ID
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            self._ensure_cursor()
            self.cursor.execute(query, list(data.values()))
            self.connection.commit()
            
            logging.info(f"数据成功插入到表 {table}")
            return self.cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            logging.error(f"插入数据失败: {str(e)}")
            raise
            
    def execute_update(self, table: str, data: Dict[str, Any], condition: str, condition_params: tuple = None) -> int:
        """
        执行更新操作
        
        Args:
            table: 表名
            data: 要更新的数据字典，键为列名，值为列值
            condition: WHERE条件语句
            condition_params: 条件参数元组（可选）
            
        Returns:
            int: 受影响的行数
        """
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
            
            params = list(data.values())
            if condition_params:
                params.extend(condition_params)
            
            self._ensure_cursor()
            self.cursor.execute(query, params)
            self.connection.commit()
            
            affected_rows = self.cursor.rowcount
            logging.info(f"成功更新表 {table} 中的 {affected_rows} 行数据")
            return affected_rows
        except Exception as e:
            self.connection.rollback()
            logging.error(f"更新数据失败: {str(e)}")
            raise
            
    def execute_delete(self, table: str, condition: str, condition_params: tuple = None) -> int:
        """
        执行删除操作
        
        Args:
            table: 表名
            condition: WHERE条件语句
            condition_params: 条件参数元组（可选）
            
        Returns:
            int: 受影响的行数
        """
        try:
            query = f"DELETE FROM {table} WHERE {condition}"
            
            self._ensure_cursor()
            self.cursor.execute(query, condition_params)
            self.connection.commit()
            
            affected_rows = self.cursor.rowcount
            logging.info(f"成功从表 {table} 中删除 {affected_rows} 行数据")
            return affected_rows
        except Exception as e:
            self.connection.rollback()
            logging.error(f"删除数据失败: {str(e)}")
            raise
            
    def close(self) -> None:
        """关闭游标"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            logging.info("数据库游标已关闭")
        except Exception as e:
            logging.error(f"关闭数据库游标失败: {str(e)}")
            raise 