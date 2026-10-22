"""留言板接口：列表 / 发表 / 点赞。"""
from flask import Blueprint
from ..extensions import db
from ..models import Guest
from .utils import ok, err, get_json, client_id, commit

bp = Blueprint('guests', __name__)


@bp.route('/guests', methods=['GET'])
def list_guests():
    guests = Guest.query.order_by(Guest.date.desc(), Guest.id.desc()).all()
    return ok([g.to_dict() for g in guests])


@bp.route('/guests', methods=['POST'])
def create_guest():
    data = get_json()
    name = (data.get('name') or '').strip()
    content = (data.get('content') or '').strip()
    if not name:
        return err('请填写昵称')
    if len(content) < 2:
        return err('留言内容太短')

    from ..models import new_id
    guest = Guest(
        id=new_id('g'),
        name=name[:40],
        color=int(data.get('color') or 0),
        content=content[:1000],
    )
    db.session.add(guest)
    commit()
    return ok(guest.to_dict())


@bp.route('/guests/<guest_id>/like', methods=['POST'])
def like_guest(guest_id):
    guest = db.session.get(Guest, guest_id)
    if not guest:
        return err('留言不存在', 404)
    from ..models import GuestLike
    cid = client_id()
    existed = GuestLike.query.filter_by(client=cid, guest_id=guest_id).first()
    if existed:
        db.session.delete(existed)
        guest.likes = max(0, (guest.likes or 0) - 1)
        liked = False
    else:
        db.session.add(GuestLike(client=cid, guest_id=guest_id))
        guest.likes = (guest.likes or 0) + 1
        liked = True
    commit()
    return ok({'liked': liked, 'likes': guest.likes})
