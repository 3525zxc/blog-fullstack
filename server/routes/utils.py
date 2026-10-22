"""路由公共工具：客户端标识、Token 认证、错误响应。"""
from functools import wraps
from flask import request, jsonify
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from ..extensions import db


def client_id():
    """前端每个浏览器生成一个匿名 ID，用于点赞/收藏的归属记录。"""
    return request.headers.get('X-Client-Id', 'anonymous')


def ok(data=None, **extra):
    payload = {'ok': True}
    if data is not None:
        payload['data'] = data
    payload.update(extra)
    return jsonify(payload)


def err(message, status=400):
    return jsonify({'ok': False, 'error': message}), status


def _serializer():
    from flask import current_app
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt='linblog-login')


def make_token(admin_id):
    return _serializer().dumps({'uid': admin_id})


def verify_token(token, max_age=None):
    from flask import current_app
    ttl = max_age or current_app.config['TOKEN_TTL']
    return _serializer().loads(token, max_age=ttl)


def admin_required(f):
    """管理接口鉴权：请求头 Authorization: Bearer <token>"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        header = request.headers.get('Authorization', '')
        token = header[7:].strip() if header.startswith('Bearer ') else ''
        if not token:
            return err('未登录', 401)
        try:
            verify_token(token)
        except (BadSignature, SignatureExpired):
            return err('登录已过期，请重新登录', 401)
        return f(*args, **kwargs)
    return wrapper


def get_json():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def commit():
    db.session.commit()
