# src/db_connector.py
import pymysql  # <-- 1. 修改 import
import pymysql.cursors

# --- 数据库配置 ---
DB_CONFIG = {
    'user': 'root',
    'password': '050326',
    'host': 'localhost',
    'database': 'lab_management_python',
    # 注意：PyMySQL 不使用 'auth_plugin'，所以确保它已被删除
}


def get_db_connection():
    """建立并返回一个数据库连接"""
    try:
        # <-- 2. 修改 connect 函数
        conn = pymysql.connect(
            **DB_CONFIG,
            cursorclass=pymysql.cursors.DictCursor  # 这是一个好习惯，让查询返回字典
        )
        return conn
    except pymysql.Error as err:  # <-- 3. 捕获 pymysql.Error
        # PyMySQL 会在这里打印一个非常清晰的错误！
        print(f"Error connecting to database: {err}")
        return None