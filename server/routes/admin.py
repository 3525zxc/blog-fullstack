"""管理接口：数据导出 / 导入 / 重置。"""
from flask import Blueprint, request
from ..extensions import db
from ..models import (Category, Sub, Post, Comment, Guest, Setting, Admin,
                      PostLike, PostCollect, CommentLike, GuestLike)
from .utils import ok, err, get_json, admin_required, commit

bp = Blueprint('admin', __name__)


def _dump():
    return {
        'settings': {r.key: r.value for r in Setting.query.all()},
        'cats': [{
            'id': c.id, 'name': c.name, 'icon': c.icon, 'desc': c.desc, 'sort': c.sort,
            'subs': [{'id': s.id, 'name': s.name, 'desc': s.desc} for s in c.subs]
        } for c in Category.query.order_by(Category.sort).all()],
        'posts': [p.to_dict() for p in Post.query.all()],
        'comments': [c.to_dict() for c in Comment.query.all()],
        'guests': [g.to_dict() for g in Guest.query.all()],
    }


@bp.route('/export', methods=['GET'])
@admin_required
def export_data():
    return ok(_dump())


@bp.route('/import', methods=['POST'])
@admin_required
def import_data():
    data = get_json()
    if not isinstance(data.get('posts'), list):
        return err('数据格式不正确：缺少 posts 字段')

    # 清空现有数据后按导入内容重建
    for model in (PostLike, PostCollect, CommentLike, GuestLike):
        model.query.delete()
    Comment.query.delete()
    Post.query.delete()
    Sub.query.delete()
    Category.query.delete()
    Guest.query.delete()
    Setting.query.delete()

    for s in data.get('settings', {}).items():
        db.session.add(Setting(key=s[0], value=str(s[1])))

    for c in data.get('cats', []):
        db.session.add(Category(id=c['id'], name=c['name'], icon=c.get('icon', 'file'),
                                desc=c.get('desc', ''), sort=c.get('sort', 0)))
        db.session.flush()
        for sub in c.get('subs', []):
            db.session.add(Sub(id=sub['id'], name=sub['name'],
                               desc=sub.get('desc', ''), cat_id=c['id']))
    db.session.flush()

    for p in data.get('posts', []):
        db.session.add(Post(
            id=p['id'], title=p['title'], excerpt=p.get('excerpt', ''),
            content=p.get('content', ''), cat=p['cat'], tags=p.get('tags', []),
            cover=p.get('cover', 0), status=p.get('status', 'published'),
            date=p.get('date', ''), views=p.get('views', 0), likes=p.get('likes', 0),
            local=p.get('local', False)))
    db.session.flush()

    for c in data.get('comments', []):
        db.session.add(Comment(
            id=c['id'], post_id=c['postId'], parent=c.get('parent'),
            name=c['name'], color=c.get('color', 0), content=c['content'],
            date=c.get('date', ''), status=c.get('status', 'approved'),
            likes=c.get('likes', 0)))
    db.session.flush()

    for g in data.get('guests', []):
        db.session.add(Guest(id=g['id'], name=g['name'], color=g.get('color', 0),
                             content=g['content'], date=g.get('date', ''),
                             likes=g.get('likes', 0)))
    db.session.flush()

    commit()
    return ok({'imported': len(data.get('posts', []))})


@bp.route('/reset', methods=['POST'])
@admin_required
def reset_data():
    for model in (PostLike, PostCollect, CommentLike, GuestLike):
        model.query.delete()
    Comment.query.delete()
    Post.query.delete()
    Sub.query.delete()
    Category.query.delete()
    Guest.query.delete()
    Setting.query.delete()
    Admin.query.delete()   # 一并清掉，避免重建管理员时唯一约束冲突
    commit()

    from ..seed import seed_all
    seed_all()
    return ok({'reset': True})
