# MySQL MCP 服务器

这是一个基于FastMCP框架开发的MySQL数据库查询服务器，提供简单易用的数据库操作接口。

## 功能特点

- 支持SQL查询和更新操作
- 使用环境变量进行数据库配置
- 提供异常处理和错误日志
- 支持参数化查询，防止SQL注入

## 环境要求

- Python >= 3.10
- uv包管理器

## 依赖库

- fastmcp >= 2.3.3
- pymysql >= 1.1.1

## 安装步骤

1. 确保已安装uv包管理器
2. 克隆项目到本地
3. 在项目根目录执行：
   ```bash
   uv init
   uv add fastmcp
   uv add pymysql
   ```

## 配置说明

在项目根目录创建`.env`文件，配置以下环境变量：

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
MYSQL_CHARSET=utf8mb4
```

## 使用方法

### 启动服务器

```bash
python Mysql.py
```

### 可用工具函数

1. query - 执行SQL查询
   ```python
   # 示例
   query("SELECT * FROM users WHERE age > ?", [18])
   ```

2. execute - 执行SQL更新操作
   ```python
   # 示例
   execute("UPDATE users SET name = ? WHERE id = ?", ["新名字", 1])
   ```

## MCP配置

在MCP配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "mysql": {
      "command": "uv",
      "args": [
        "--directory",
        "Mysql",
        "run",
        "Mysql.py"
      ],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "your_password",
        "MYSQL_DATABASE": "your_database",
        "MYSQL_CHARSET": "utf8mb4"
      }
    }
  }
}
```

配置说明：
- `command`: 使用uv包管理器运行Python脚本
- `args`: 运行参数配置
  - `--directory`: 指定运行目录
  - `run`: 运行Python脚本
- `env`: 环境变量配置，与`.env`文件中的配置对应

## 注意事项

- 确保数据库配置正确且数据库服务器可访问
- 建议在生产环境中使用安全的密码存储方式
- 定期检查和维护数据库连接
