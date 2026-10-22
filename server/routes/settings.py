"""站点设置接口：读取 / 保存。"""
from flask import Blueprint
from ..extensions import db
from ..models import Setting
from .utils import ok, err, get_json, admin_required, commit

bp = Blueprint('settings', __name__)

DEFAULTS = {
    'siteName': '林间漫记',
    'sub': '记录代码、设计与生活的交汇点',
    'author': '大谢',
    'sign': '前端工程师 / 业余摄影爱好者',
    'intro': '你好，我是大谢。白天写前端，晚上写文字，周末按快门。这里是我的数字自留地，记录技术笔记、设计观察与生活切片。',
    'accent': '#5b5bd6',
    'startedAt': '2024-03-01',
}

ALLOWED_KEYS = set(DEFAULTS.keys())


def load_settings():
    rows = Setting.query.all()
    data = dict(DEFAULTS)
    for r in rows:
        data[r.key] = r.value
    return data


@bp.route('', methods=['GET'])
@bp.route('/', methods=['GET'])
def get_settings():
    return ok(load_settings())


@bp.route('', methods=['PUT'])
@bp.route('/', methods=['PUT'])
@admin_required
def save_settings():
    data = get_json()
    if not data:
        return err('没有需要保存的内容')
    for key, value in data.items():
        if key not in ALLOWED_KEYS:
            continue
        row = db.session.get(Setting, key)
        if row:
            row.value = str(value)
        else:
            db.session.add(Setting(key=key, value=str(value)))
    commit()
    return ok(load_settings())
