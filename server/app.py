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

    with app.app_context():
        db.create_all()
        _seed_if_empty()

    _register_static(app)
    _register_error_handlers(app)
    return app


def _seed_if_empty():
    from server.models import Admin, Category
    if Admin.query.count() == 0 and Category.query.count() == 0:
        from server.seed import seed_all
        seed_all()
        print('[init] 数据库为空，已写入演示数据（admin / admin123）')


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
        return jsonify({'ok': True})


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
