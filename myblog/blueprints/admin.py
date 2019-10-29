from flask import Blueprint, render_template, url_for,flash, redirect, request, current_app
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from myblog.models import Post, Admin, Category, Tag, Comment
from myblog.utils import redirect_back
from myblog.forms import PostForm, AdminAboutForm
from myblog.plugins import db
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()


@admin_bp.route('/new_post', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        category_name = request.form.get('categories')
        category = Category.query.filter(Category.name == category_name).first()
        if category is None:
            category = Category(name=category_name)
            db.session.add(category)

        tags = []
        for tag_name in request.form.getlist('tags'):
            tag = Tag.query.filter(Tag.name == tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            tags.append(tag)
        post = Post()
        post.title = form.title.data
        post.body = form.body.data
        post.tags = tags
        post.category = category
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.show_post',post_id=post.id))

    categories = Category.query.all()
    tags = Tag.query.all()
    return render_template('admin/new_post.html', form=form, categories=categories, tags=tags)


@admin_bp.route('/manage_post')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['MYBLOG_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('posts/archive.html', page=page, pagination=pagination, posts=posts)



@admin_bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    categories = Category.query.all()
    tags = Tag.query.all()
    if form.validate_on_submit():
        category_name = request.form.get('categories')
        category = Category.query.filter(Category.name == category_name).first()
        if category is None:
            category = Category(name=category_name)
            db.session.add(category)

        tags = []
        for tag_name in request.form.getlist('tags'):
            tag = Tag.query.filter(Tag.name == tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            tags.append(tag)

        post.title = form.title.data
        post.body = form.body.data
        post.tags = tags
        post.category = category
        db.session.add(post)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('main.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('admin/edit_post.html', form=form, categories=categories, tags=tags,post=post)


@admin_bp.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()


@admin_bp.route('/set_comment/<int:post_id>', methods=['POST'])
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    post.can_comment = not post.can_comment
    db.session.add(post)
    db.session.commit()
    return redirect_back()


@admin_bp.route('/manage_comment', methods = ['GET', 'POST'])
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')  # 'all', 'unreviewed', 'admin'
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query

    unread_comments_count = Comment.query.filter_by(reviewed=False).count()

    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', comments=comments, pagination=pagination,unread_comments_count=unread_comments_count)


@admin_bp.route('/approve_comment/<int:comment_id>', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('Comment published.', 'success')
    return redirect_back()


@admin_bp.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if category_id == 1:
        flash('默认分类不能删除', 'warning')
        return redirect_back()

    category = Category.query.get_or_404(category_id)
    category.delete()
    flash('分类{}删除成功.'.format(category.name), 'success')
    return redirect_back()


@admin_bp.route('/manage_category')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/add_category',methods=['POST'])
@login_required
def add_category():
    name = request.form.get('new_category')
    category = Category(name=name)
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return redirect(url_for('main.show_all_categories'))


@admin_bp.route('/delete_tag/<int:tag_id>', methods=['POST'])
@login_required
def delete_tag(tag_id):
    if tag_id == 1:
        flash('默认标签不能删除', 'warning')
        return redirect_back()
    tag = Tag.query.get_or_404(tag_id)
    tag.delete()
    flash('标签{}删除成功.'.format(tag.name), 'success')
    return redirect_back()


@admin_bp.route('/manage_tag')
@login_required
def manage_tag():
    return render_template('posts/tags.html')


@admin_bp.route('/add_tag', methods=['POST'])
@login_required
def add_tag():
    name = request.form.get('new_tag')
    tag = Tag(name=name)
    db.session.add(tag)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return redirect(url_for('main.show_all_tags'))


@admin_bp.route('/edit_about', methods=['GET','POST'])
@login_required
def edit_about():
    form = AdminAboutForm()
    admin = Admin.query.first_or_404()
    if form.validate_on_submit():
        from myblog.plugins import mistune_md
        admin.about_title = form.title.data
        admin.about = form.body.data
        admin.about_html = mistune_md(form.body.data)
        db.session.commit()
        return redirect(url_for('main.about_me'))
    form.title.data = admin.about_title
    form.body.data = admin.about
    return render_template('admin/edit_about.html', form=form)

