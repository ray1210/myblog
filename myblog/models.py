from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from markdown import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from myblog.plugins import db, md


association_table = db.Table('association', db.Column('post_id', db.Integer, db.ForeignKey('tag.id')),
                             db.Column('tag_id', db.Integer, db.ForeignKey('post.id')))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    posts = db.relationship('Post', back_populates='category')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read_count = db.Column(db.Integer, default=0)
    can_comment = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    tags = db.relationship('Tag', secondary=association_table, back_populates='posts')
    comments = db.relationship('Comment',back_populates='post',cascade='all, delete-orphan')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = md.convert(value)
        md.reset()


db.event.listen(Post.body, 'set', Post.on_changed_body)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    posts = db.relationship('Post', secondary=association_table, back_populates='tags')


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), unique=True, nullable=False)

    @property
    def password(self):
        pass

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])


