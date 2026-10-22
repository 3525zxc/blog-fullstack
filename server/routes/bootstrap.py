"""聚合接口：一次性返回前端需要的全部数据（保持与原前端数据层同构）。"""
from flask import Blueprint, request
from ..extensions import db
from ..models import (Category, Sub, Post, Comment, Guest, PostLike, PostCollect,
                      CommentLike, GuestLike)
from .utils import ok, client_id, verify_token

bp = Blueprint('bootstrap', __name__)


def _is_admin():
    header = request.headers.get('Authorization', '')
    token = header[7:].strip() if header.startswith('Bearer ') else ''
    if not token:
        return False
    try:
        verify_token(token)
        return True
    except Exception:
        return False


@bp.route('/bootstrap', methods=['GET'])
def bootstrap():
    cid = client_id()
    is_admin = _is_admin()

    cats = []
    for c in Category.query.order_by(Category.sort).all():
        cats.append({
            'id': c.id, 'name': c.name, 'icon': c.icon, 'desc': c.desc,
            'subs': [{'id': s.id, 'name': s.name, 'desc': s.desc,
                      'main': c.id, 'mainName': c.name} for s in c.subs]
        })

    post_query = Post.query if is_admin else Post.query.filter_by(status='published')
    posts = post_query.order_by(Post.date.desc(), Post.created_at.desc()).all()

    comment_query = Comment.query if is_admin else Comment.query.filter_by(status='approved')
    comments = comment_query.order_by(Comment.date.desc(), Comment.id.desc()).all()

    guests = Guest.query.order_by(Guest.date.desc(), Guest.id.desc()).all()

    likes = {}
    for row in PostLike.query.filter_by(client=cid).all():
        likes[row.post_id] = 1
    comment_likes = {}
    for row in CommentLike.query.filter_by(client=cid).all():
        comment_likes[row.comment_id] = 1
    guest_likes = {}
    for row in GuestLike.query.filter_by(client=cid).all():
        guest_likes[row.guest_id] = 1

    from .settings import load_settings
    return ok({
        'settings': load_settings(),
        'cats': cats,
        'posts': [p.to_dict() for p in posts],
        'comments': [c.to_dict() for c in comments],
        'guests': [g.to_dict() for g in guests],
        'meta': {
            'likes': likes,
            'collects': [r.post_id for r in PostCollect.query.filter_by(client=cid).all()],
            'commentLikes': comment_likes,
            'guestLikes': guest_likes,
        },
    })
