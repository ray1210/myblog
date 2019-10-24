from flask import Blueprint, render_template, url_for, request, current_app, redirect, flash
from flask_login import current_user
from myblog.models import Post, Category, Tag, Comment
from myblog.plugins import db, md
from myblog.forms import CommentForm, AdminCommentForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('index.html', pagination=pagination, posts=posts)


@main_bp.route('/show_post/<int:post_id>', methods = ['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.username
        form.email.data = current_app.config['MYBLOG_EMAIL']
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('评论发布成功', 'success')
        else:
            flash('您的评论将在管理员审核后发布', 'info')
        return redirect(url_for('main.show_post', post_id=post_id))
    if request.args.get('from_index') == 'True':
        post.read_count += 1
        db.session.add(post)
        db.session.commit()
    return render_template('posts/post.html', post=post, pagination=pagination, form=form, comments=comments)

@main_bp.route('/reply_comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('Comment is disabled.', 'warning')
        return redirect(url_for('main.show_post', post_id=comment.post.id))
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


@main_bp.route('/show_category/<int:category_id>')
def show_category(category_id):
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PER_PAGE']
    pagination = Post.query.filter_by(category_id=category_id).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('index.html', pagination=pagination, posts=posts)


@main_bp.route('/show_tag/<int:tag_id>')
def show_tag(tag_id):
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PER_PAGE']
    Post.query.filter(Post.tags.any(id=tag_id))
    pagination = Post.query.filter(Post.tags.any(id=tag_id)).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('index.html', pagination=pagination, posts=posts)


@main_bp.route('/about_me')
def about_me():
    about_me_md = current_app.config['MYBLOG_ABOUT_ME']
    about_me_html = md.convert(current_app.config['MYBLOG_ABOUT_ME'])
    md.reset()
    return render_template('about_me.html', about_me_html = about_me_html)
