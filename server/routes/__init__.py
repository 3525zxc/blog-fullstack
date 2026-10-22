"""路由包初始化：统一注册蓝图。"""
from . import auth, posts, comments, guests, categories, settings, admin, bootstrap


def register_blueprints(app):
    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(bootstrap.bp, url_prefix='/api')
    app.register_blueprint(posts.bp, url_prefix='/api/posts')
    app.register_blueprint(comments.bp, url_prefix='/api')
    app.register_blueprint(guests.bp, url_prefix='/api')
    app.register_blueprint(categories.bp, url_prefix='/api/categories')
    app.register_blueprint(settings.bp, url_prefix='/api/settings')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')
