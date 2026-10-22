"""数据库连接自检工具。

用法（在项目根目录）：
    python -m server.check_db

读取 .env / 环境变量中的连接配置，尝试连接 MySQL 并打印明确结果。
部署到 suga.app 前先在本地跑一遍，可避免“容器里连不上库”类问题。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.config import Config  # noqa: E402


def main():
    uri = Config.SQLALCHEMY_DATABASE_URI
    # 隐藏密码，避免截图泄露
    safe_uri = uri
    if '@' in uri:
        head, tail = uri.split('@', 1)
        if ':' in head:
            scheme_user = head.rsplit(':', 1)[0]
            safe_uri = scheme_user + ':***@' + tail
    print('连接目标：' + safe_uri)

    if not Config.is_mysql():
        print('⚠️  当前不是 MySQL 连接串（DATABASE_URL 未设置或指向其他数据库）')

    try:
        import pymysql
        from urllib.parse import urlparse, unquote
        u = urlparse(uri)
        conn = pymysql.connect(
            host=u.hostname or '127.0.0.1',
            port=int(u.port or 3306),
            user=unquote(u.username or 'root'),
            password=unquote(u.password or ''),
            database=(u.path or '/').lstrip('/') or None,
            charset='utf8mb4',
            connect_timeout=10,
        )
        with conn.cursor() as cur:
            cur.execute('SELECT VERSION()')
            version = cur.fetchone()[0]
        conn.close()
        print('✅ 数据库连接成功！MySQL 版本：' + str(version))
        print('   可以启动博客了：python server/app.py')
        return 0
    except ImportError:
        print('❌ 未安装 PyMySQL，请先执行：pip install -r requirements.txt')
        return 1
    except Exception as e:
        print('❌ 连接失败：' + str(e))
        print()
        print('请逐项检查：')
        print('  1. .env 里的 MYSQL_HOST / MYSQL_PORT / MYSQL_USER / MYSQL_PASSWORD / MYSQL_DB 是否和 sqlpub 控制台一致')
        print('  2. sqlpub 控制台里实例状态是否为“正常”')
        print('  3. 密码是否保存正确（只显示一次，忘了就重置）')
        print('  4. 端口是否照抄（有的实例是 3307 不是 3306）')
        print('  5. 本机网络能否访问外网 3306/3307 端口（公司网可能拦截）')
        return 1


if __name__ == '__main__':
    sys.exit(main())
