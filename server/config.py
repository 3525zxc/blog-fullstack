"""应用配置：默认 MySQL，全部支持环境变量覆盖，方便部署到 suga.app / 接入 sqlpub。

本地开发：复制 .env.example 为 .env 并填写连接信息（.env 不会进 git）。
部署到 suga.app：在 Config → Environment Variables 里设置同样的变量。
"""
import os
from urllib.parse import quote_plus

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def _load_dotenv():
    """极简 .env 加载（避免引入 python-dotenv 依赖）。"""
    path = os.path.join(BASE_DIR, '.env')
    if not os.path.isfile(path):
        return
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        pass


_load_dotenv()


def _mysql_uri():
    """由离散环境变量拼装 MySQL 连接串（密码自动 URL 编码）。"""
    user = quote_plus(os.environ.get('MYSQL_USER', 'root'))
    password = quote_plus(os.environ.get('MYSQL_PASSWORD', ''))
    host = os.environ.get('MYSQL_HOST', '127.0.0.1')
    port = os.environ.get('MYSQL_PORT', '3306')
    name = os.environ.get('MYSQL_DB', 'linblog')
    return 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(user, password, host, port, name)


class Config:
    # 生产环境务必通过环境变量设置强随机 SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-please-change-me')

    # 数据库：默认 MySQL（本地或 sqlpub 均可）；
    # 也可用 DATABASE_URL 指向任何 SQLAlchemy 支持的数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or _mysql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Token 有效期（秒）
    TOKEN_TTL = int(os.environ.get('TOKEN_TTL', 7 * 24 * 3600))

    # 跨域（前端单独部署时才需要；同源部署无影响）
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    @staticmethod
    def is_mysql(uri=None):
        uri = uri or Config.SQLALCHEMY_DATABASE_URI
        return uri.startswith('mysql')


# MySQL 连接池参数（sqlpub 免费版仅 30 个连接，需控制池大小）
MYSQL_ENGINE_OPTIONS = {
    'pool_recycle': 280,      # 短于 MySQL wait_timeout，避免连接被服务端断开
    'pool_pre_ping': True,    # 取出连接前先探活
    'pool_size': 3,
    'max_overflow': 2,
}
