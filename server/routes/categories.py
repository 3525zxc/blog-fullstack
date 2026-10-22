"""分类接口：列表（含文章数）/ 新增二级分类 / 删除二级分类。"""
from flask import Blueprint
from ..extensions import db
from ..models import Category, Sub, Post
from .utils import ok, err, get_json, admin_required, commit

bp = Blueprint('categories', __name__)


@bp.route('', methods=['GET'])
@bp.route('/', methods=['GET'])
def list_categories():
    cats = Category.query.order_by(Category.sort).all()
    result = []
    for c in cats:
        subs = []
        for s in c.subs:
            count = Post.query.filter_by(cat=s.id, status='published').count()
            subs.append({'id': s.id, 'name': s.name, 'desc': s.desc,
                         'main': c.id, 'mainName': c.name})
        total = Post.query.filter(Post.cat.in_([s['id'] for s in subs]),
                                  Post.status == 'published').count()
        result.append({'id': c.id, 'name': c.name, 'icon': c.icon,
                       'desc': c.desc, 'subs': subs, 'total': total})
    return ok(result)


@bp.route('/subs', methods=['POST'])
@admin_required
def add_sub():
    data = get_json()
    main_id = (data.get('mainId') or '').strip()
    name = (data.get('name') or '').strip()
    if not name:
        return err('分类名称不能为空')
    if len(name) > 20:
        return err('分类名称过长')
    main = db.session.get(Category, main_id)
    if not main:
        return err('主分类不存在', 404)

    from ..models import new_id
    sub = Sub(id=new_id('custom-'), name=name, desc='自定义分类', cat_id=main_id)
    db.session.add(sub)
    commit()
    return ok({'id': sub.id, 'name': sub.name, 'desc': sub.desc,
               'main': main_id, 'mainName': main.name})


@bp.route('/subs/<sub_id>', methods=['DELETE'])
@admin_required
def delete_sub(sub_id):
    sub = db.session.get(Sub, sub_id)
    if not sub:
        return err('分类不存在', 404)
    db.session.delete(sub)
    commit()
    return ok()
