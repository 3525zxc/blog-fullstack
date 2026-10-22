"""认证接口：登录 / 当前身份 / 退出。"""
from flask import Blueprint, request
from ..extensions import db
from ..models import Admin
from .utils import ok, err, get_json, make_token, verify_token, admin_required

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    data = get_json()
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    if not username or not password:
        return err('请输入账号和密码')

    admin = Admin.query.filter_by(username=username).first()
    if not admin or not admin.check_password(password):
        return err('账号或密码错误', 401)

    token = make_token(admin.id)
    return ok({'token': token, 'user': {'id': admin.id, 'username': admin.username}})


@bp.route('/me', methods=['GET'])
def me():
    header = request.headers.get('Authorization', '')
    token = header[7:].strip() if header.startswith('Bearer ') else ''
    if not token:
        return err('未登录', 401)
    try:
        data = verify_token(token)
    except Exception:
        return err('登录已过期，请重新登录', 401)
    admin = db.session.get(Admin, data['uid'])
    if not admin:
        return err('账号不存在', 401)
    return ok({'id': admin.id, 'username': admin.username})


@bp.route('/logout', methods=['POST'])
def logout():
    # Token 为无状态设计，客户端删除即可
    return ok()
