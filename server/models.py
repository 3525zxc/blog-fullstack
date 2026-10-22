"""SQLAlchemy ORM 模型。

表结构：
  categories / subs      分类体系（主分类 -> 二级分类）
  posts                  文章
  comments               评论（支持 parent 一级回复）
  guests                 留言板
  settings               站点设置（键值对）
  admins                 管理员（密码哈希）
  *_likes / collects     点赞与收藏（按浏览器 client_id 记录，无需登录）
"""
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


def new_id(prefix):
    return prefix + datetime.utcnow().strftime('%Y%m%d%H%M%S%f')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    icon = db.Column(db.String(40), default='file')
    desc = db.Column(db.String(160), default='')
    sort = db.Column(db.Integer, default=0)
    subs = db.relationship('Sub', backref='category', lazy=True,
                           cascade='all, delete-orphan', order_by='Sub.id')


class Sub(db.Model):
    __tablename__ = 'subs'
    id = db.Column(db.String(48), primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    desc = db.Column(db.String(160), default='')
    cat_id = db.Column(db.String(40), db.ForeignKey('categories.id'), nullable=False,
                       index=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'desc': self.desc}


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.String(48), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.String(600), default='')
    content = db.Column(db.Text, default='')
    cat = db.Column(db.String(48), db.ForeignKey('subs.id'), nullable=False, index=True)
    tags = db.Column(db.JSON, default=list)
    cover = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='published', index=True)
    date = db.Column(db.String(10), default='', index=True)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    local = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'excerpt': self.excerpt,
            'content': self.content, 'cat': self.cat,
            'tags': list(self.tags or []), 'cover': self.cover or 0,
            'status': self.status, 'date': self.date,
            'views': self.views or 0, 'likes': self.likes or 0,
            'local': bool(self.local)
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(48), primary_key=True)
    post_id = db.Column(db.String(48), db.ForeignKey('posts.id'), nullable=False, index=True)
    parent = db.Column(db.String(48), nullable=True)
    name = db.Column(db.String(40), nullable=False)
    color = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(10), default='')
    status = db.Column(db.String(20), default='approved', index=True)
    likes = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id, 'postId': self.post_id, 'parent': self.parent,
            'name': self.name, 'color': self.color or 0, 'content': self.content,
            'date': self.date, 'status': self.status, 'likes': self.likes or 0
        }


class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.String(48), primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    color = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(10), default='')
    likes = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'color': self.color or 0,
            'content': self.content, 'date': self.date, 'likes': self.likes or 0
        }


class Setting(db.Model):
    __tablename__ = 'settings'
    key = db.Column(db.String(40), primary_key=True)
    value = db.Column(db.Text, default='')


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)


class PostLike(db.Model):
    __tablename__ = 'post_likes'
    client = db.Column(db.String(48), primary_key=True)
    post_id = db.Column(db.String(48), db.ForeignKey('posts.id'), primary_key=True)


class PostCollect(db.Model):
    __tablename__ = 'post_collects'
    client = db.Column(db.String(48), primary_key=True)
    post_id = db.Column(db.String(48), db.ForeignKey('posts.id'), primary_key=True)


class CommentLike(db.Model):
    __tablename__ = 'comment_likes'
    client = db.Column(db.String(48), primary_key=True)
    comment_id = db.Column(db.String(48), db.ForeignKey('comments.id'), primary_key=True)


class GuestLike(db.Model):
    __tablename__ = 'guest_likes'
    client = db.Column(db.String(48), primary_key=True)
    guest_id = db.Column(db.String(48), db.ForeignKey('guests.id'), primary_key=True)
