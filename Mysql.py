from mcp.server.fastmcp import FastMCP
from typing import Any, Dict, List, Optional
from pymysql import connect
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import os

class MySQLMCP:
    def __init__(self):
        # 加载.env文件中的环境变量
        load_dotenv()
        
        # 从环境变量中读取数据库配置
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'localhost'),
            'port': int(os.getenv('MYSQL_PORT', '3306')),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_DATABASE', ''),
            'charset': os.getenv('MYSQL_CHARSET', 'utf8mb4'),
            'cursorclass': DictCursor
        }
        self.connection = None
        self.mcp = FastMCP("MySQL MCP Server")
        self._setup_tools()

    def connect(self) -> None:
        """建立数据库连接"""
        try:
            self.connection = connect(**self.config)
        except Exception as e:
            raise Exception(f"数据库连接失败: {str(e)}")

    def _setup_tools(self) -> None:
        """设置MCP工具函数"""
        @self.mcp.tool()
        def query(sql: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
            """
            执行SQL查询
            """
            if not self.connection:
                self.connect()
            try:
                with self.connection.cursor() as cursor:
                    print(f"执行SQL查询: {sql}")
                    cursor.execute(sql, params or ())
                    result = cursor.fetchall()
                    print(f"查询结果: {result}")
                    return result
            except Exception as e:
                error_msg = f"查询执行失败: {str(e)}"
                print(error_msg)
                raise Exception(error_msg)

        @self.mcp.tool()
        def execute(sql: str, params: Optional[List[Any]] = None) -> int:
            """执行SQL更新操作"""
            if not self.connection:
                self.connect()
            try:
                with self.connection.cursor() as cursor:
                    affected_rows = cursor.execute(sql, params or ())
                    self.connection.commit()
                    return affected_rows
            except Exception as e:
                self.connection.rollback()
                raise Exception(f"执行失败: {str(e)}")

    def run(self, transport: str = 'stdio') -> None:
        """启动MCP服务器"""
        self.mcp.run(transport=transport)

if __name__ == "__main__":
    # 示例用法 - 现在会从.env文件读取配置
    mysql_mcp = MySQLMCP()
    mysql_mcp.run()