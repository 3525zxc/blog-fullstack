"""文章接口：列表 / 详情 / 浏览计数 / 增删改 / 状态切换。"""
from flask import Blueprint, request
from ..extensions import db
from ..models import Post, Comment
from .utils import ok, err, get_json, admin_required, commit, client_id

bp = Blueprint('posts', __name__)


def _visible_filter(query, args):
    """未登录访客只能看到已发布文章；管理员可显式查看全部。"""
    from .utils import verify_token
    header = request.headers.get('Authorization', '')
    token = header[7:].strip() if header.startswith('Bearer ') else ''
    is_admin = False
    if token:
        try:
            verify_token(token)
            is_admin = True
        except Exception:
            is_admin = False
    # 默认只看已发布；status=all 仅对管理员生效
    status = args.get('status', '') or 'published'
    if status == 'all':
        status = 'all' if is_admin else 'published'
    if status and status != 'all':
        query = query.filter(Post.status == status)
    return query


@bp.route('', methods=['GET'])
@bp.route('/', methods=['GET'])
def list_posts():
    query = Post.query
    query = _visible_filter(query, request.args)

    cat = request.args.get('cat', '')
    if cat:
        query = query.filter(Post.cat == cat)

    main = request.args.get('main', '')
    if main:
        from ..models import Sub
        sub_ids = [s.id for s in Sub.query.filter_by(cat_id=main).all()]
        query = query.filter(Post.cat.in_(sub_ids))

    tag = request.args.get('tag', '')
    if tag:
        # JSON 列需显式转文本后再 LIKE（MySQL 8 / SQLite 均兼容）
        query = query.filter(db.cast(Post.tags, db.Text).like('%"' + tag + '"%'))

    q = request.args.get('q', '').strip().lower()
    if q:
        like = '%' + q + '%'
        query = query.filter(db.or_(Post.title.ilike(like),
                                    Post.excerpt.ilike(like),
                                    Post.content.ilike(like)))

    posts = query.order_by(Post.date.desc(), Post.created_at.desc()).all()
    return ok([p.to_dict() for p in posts])


@bp.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return err('文章不存在', 404)
    return ok(post.to_dict())


@bp.route('/<post_id>/view', methods=['POST'])
def add_view(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return err('文章不存在', 404)
    post.views = (post.views or 0) + 1
    commit()
    return ok({'views': post.views})


@bp.route('/<post_id>/like', methods=['POST'])
def like_post(post_id):
    from ..models import PostLike
    post = db.session.get(Post, post_id)
    if not post:
        return err('文章不存在', 404)
    cid = client_id()
    existed = PostLike.query.filter_by(client=cid, post_id=post_id).first()
    if existed:
        db.session.delete(existed)
        post.likes = max(0, (post.likes or 0) - 1)
        liked = False
    else:
        db.session.add(PostLike(client=cid, post_id=post_id))
        post.likes = (post.likes or 0) + 1
        liked = True
    commit()
    return ok({'liked': liked, 'likes': post.likes})


@bp.route('/<post_id>/collect', methods=['POST'])
def collect_post(post_id):
    from ..models import PostCollect
    post = db.session.get(Post, post_id)
    if not post:
        return err('文章不存在', 404)
    cid = client_id()
    existed = PostCollect.query.filter_by(client=cid, post_id=post_id).first()
    if existed:
        db.session.delete(existed)
        collected = False
    else:
        db.session.add(PostCollect(client=cid, post_id=post_id))
        collected = True
    commit()
    return ok({'collected': collected})


@bp.route('', methods=['POST'])
@bp.route('/', methods=['POST'])
@admin_required
def create_post():
    data = get_json()
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()
    if not title:
        return err('标题不能为空')
    if not content:
        return err('正文不能为空')

    from ..models import new_id
    post = Post(
        id=new_id('p'),
        title=title,
        content=content,
        excerpt=(data.get('excerpt') or '').strip(),
        cat=data.get('cat') or 'frontend',
        tags=data.get('tags') or [],
        cover=int(data.get('cover') or 0),
        status=data.get('status') or 'published',
        date=data.get('date') or '',
        local=bool(data.get('local')),
        views=0, likes=0,
    )
    db.session.add(post)
    commit()
    return ok(post.to_dict())


@bp.route('/<post_id>', methods=['PUT'])
@admin_required
def update_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return err('文章不存在', 404)
    data = get_json()
    if 'title' in data:
        title = (data.get('title') or '').strip()
        if not title:
            return err('标题不能为空')
        post.title = title
    if 'content' in data:
        post.content = data.get('content') or ''
    if 'excerpt' in data:
        post.excerpt = (data.get('excerpt') or '').strip()
    if 'cat' in data:
        post.cat = data.get('cat')
    if 'tags' in data:
        post.tags = data.get('tags') or []
    if 'cover' in data:
        post.cover = int(data.get('cover') or 0)
    if 'status' in data:
        post.status = data.get('status') or post.status
    if 'date' in data and data.get('date'):
        post.date = data.get('date')
    commit()
    return ok(post.to_dict())


@bp.route('/<post_id>/status', methods=['PATCH'])
@admin_required
def set_status(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return err('文章不存在', 404)
    data = get_json()
    status = data.get('status')
    if status not in ('published', 'draft'):
        return err('非法的状态')
    post.status = status
    commit()
    return ok(post.to_dict())


@bp.route('/<post_id>', methods=['DELETE'])
@admin_required
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return err('文章不存在', 404)
    # 连同评论、点赞记录一起清理
    Comment.query.filter_by(post_id=post_id).delete()
    from ..models import PostLike, PostCollect
    PostLike.query.filter_by(post_id=post_id).delete()
    PostCollect.query.filter_by(post_id=post_id).delete()
    db.session.delete(post)
    commit()
    return ok()
