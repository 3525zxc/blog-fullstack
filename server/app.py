"""Flask 应用工厂 + 入口。

- 同源托管前端静态站点（web/ 目录），API 前缀 /api
- 首次启动自动建表并写入演示数据
- 兼容 gunicorn：gunicorn server.app:app
"""
import os
import sys

# 支持 `python server/app.py` 直接运行：把项目根目录加入模块搜索路径
if __package__ in (None, ''):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, send_from_directory, jsonify

from server.config import Config, MYSQL_ENGINE_OPTIONS
from server.extensions import db, cors
from server.routes import register_blueprints

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WEB_DIR = os.path.join(BASE_DIR, 'web')


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)

    if Config.is_mysql():
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = MYSQL_ENGINE_OPTIONS

    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    db.init_app(app)
    register_blueprints(app)

    _init_db_with_retry(app)

    _register_static(app)
    _register_error_handlers(app)
    return app


def _init_db_with_retry(app, retries=5, delay=3):
    """建表 + 播种；数据库暂时连不上时重试，失败则给出明确的中文提示。"""
    import time
    from server.models import Admin, Category
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with app.app_context():
                db.create_all()
                _seed_if_empty()
            return True
        except Exception as e:
            last_err = e
            print('[init] 数据库连接失败（第 %d/%d 次）：%s' % (attempt, retries, e), flush=True)
            if attempt < retries:
                time.sleep(delay)
    print('[init] ============================================================', flush=True)
    print('[init] ❌ 无法连接 MySQL 数据库，程序启动中止。', flush=True)
    print('[init] 请检查环境变量是否配置正确：', flush=True)
    print('[init]   DATABASE_URL = %s' % Config.SQLALCHEMY_DATABASE_URI.split('@')[-1], flush=True)
    print('[init] 常见原因：账号密码错误 / 主机端口写错 / sqlpub 实例未运行 /', flush=True)
    print('[init]          安全组或防火墙拦截 / 密码含特殊字符未编码', flush=True)
    print('[init] 本地排查：python -m server.check_db', flush=True)
    print('[init] ============================================================', flush=True)
    raise last_err


def _seed_if_empty():
    from server.models import Admin, Category
    try:
        need_seed = Admin.query.count() == 0 and Category.query.count() == 0
    except Exception:
        need_seed = True
    if need_seed:
        try:
            from server.seed import seed_all
            seed_all()
            print('[init] 数据库为空，已写入演示数据（admin / admin123）', flush=True)
        except Exception as e:
            # 并发启动时可能已被其他进程播种，按已播种处理
            db.session.rollback()
            print('[init] 播种被跳过或失败：%s' % e, flush=True)
            if Admin.query.count() == 0:
                raise


def _register_static(app):
    @app.route('/')
    def index():
        return send_from_directory(WEB_DIR, 'index.html')

    @app.route('/<path:filename>')
    def web_files(filename):
        full = os.path.join(WEB_DIR, filename)
        if os.path.isfile(full):
            return send_from_directory(WEB_DIR, filename)
        # 未找到的文件回退到首页（带 query 的页面路由均可用）
        return send_from_directory(WEB_DIR, 'index.html')

    @app.route('/healthz')
    def healthz():
        # 同时探测数据库：连不上库时返回 503，便于部署平台健康检查失败并暴露原因
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({'ok': True, 'db': 'up'})
        except Exception as e:
            return jsonify({'ok': False, 'db': 'down', 'error': str(e)}), 503


def _register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        from flask import request
        if request.path.startswith('/api/'):
            return jsonify({'ok': False, 'error': '接口不存在'}), 404
        return send_from_directory(WEB_DIR, 'index.html')

    @app.errorhandler(500)
    def server_error(e):
        from flask import request
        if request.path.startswith('/api/'):
            return jsonify({'ok': False, 'error': '服务器内部错误'}), 500
        return jsonify({'ok': False, 'error': '服务器内部错误'}), 500


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # 生产部署请使用 gunicorn（见 README）；此处仅用于本地开发
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG') == '1')
