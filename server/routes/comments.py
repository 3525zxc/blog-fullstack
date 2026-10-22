"""评论接口：文章评论列表 / 发表 / 点赞 / 审核 / 删除。"""
from flask import Blueprint, request
from ..extensions import db
from ..models import Comment, Post
from .utils import ok, err, get_json, client_id, admin_required, commit

bp = Blueprint('comments', __name__)


@bp.route('/posts/<post_id>/comments', methods=['GET'])
def post_comments(post_id):
    query = Comment.query.filter_by(post_id=post_id)
    # 未登录访客只看已通过审核的评论
    header = request.headers.get('Authorization', '')
    token = header[7:].strip() if header.startswith('Bearer ') else ''
    is_admin = False
    if token:
        try:
            from .utils import verify_token
            verify_token(token)
            is_admin = True
        except Exception:
            pass
    if not is_admin:
        query = query.filter(Comment.status == 'approved')
    comments = query.order_by(Comment.date.desc(), Comment.id.desc()).all()
    return ok([c.to_dict() for c in comments])


@bp.route('/comments', methods=['POST'])
def create_comment():
    data = get_json()
    post_id = (data.get('postId') or '').strip()
    name = (data.get('name') or '').strip()
    content = (data.get('content') or '').strip()
    if not post_id:
        return err('缺少文章 ID')
    if not db.session.get(Post, post_id):
        return err('文章不存在', 404)
    if not name:
        return err('请填写昵称')
    if len(content) < 2:
        return err('评论内容太短')

    from ..models import new_id
    comment = Comment(
        id=new_id('c'),
        post_id=post_id,
        parent=(data.get('parent') or None),
        name=name[:40],
        color=int(data.get('color') or 0),
        content=content[:2000],
        status='approved',   # 原型默认即时通过，可在后台下架
    )
    db.session.add(comment)
    commit()
    return ok(comment.to_dict())


@bp.route('/comments/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return err('评论不存在', 404)
    from ..models import CommentLike
    cid = client_id()
    existed = CommentLike.query.filter_by(client=cid, comment_id=comment_id).first()
    if existed:
        db.session.delete(existed)
        comment.likes = max(0, (comment.likes or 0) - 1)
        liked = False
    else:
        db.session.add(CommentLike(client=cid, comment_id=comment_id))
        comment.likes = (comment.likes or 0) + 1
        liked = True
    commit()
    return ok({'liked': liked, 'likes': comment.likes})


@bp.route('/comments/<comment_id>/status', methods=['PATCH'])
@admin_required
def set_comment_status(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return err('评论不存在', 404)
    data = get_json()
    status = data.get('status')
    if status not in ('approved', 'pending'):
        return err('非法的状态')
    comment.status = status
    commit()
    return ok(comment.to_dict())


@bp.route('/comments/<comment_id>', methods=['DELETE'])
@admin_required
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return err('评论不存在', 404)
    from ..models import CommentLike
    # 连同子回复与点赞记录一起删除
    Comment.query.filter_by(parent=comment_id).delete()
    CommentLike.query.filter_by(comment_id=comment_id).delete()
    db.session.delete(comment)
    commit()
    return ok()
