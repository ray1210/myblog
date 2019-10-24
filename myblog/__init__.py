from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from wtforms import HiddenField
from flask_migrate import Migrate
import click
from myblog.plugins import db, moment, csrf, login_manager
from myblog.config import config


def create_app(config_name = 'production'):
    app = Flask('myblog')
    app.config.from_object(config[config_name])
    app.jinja_env.add_extension('jinja2.ext.do')
    app.jinja_env.globals['bootstrap_is_hidden_field'] = bootstrap_is_hidden_field
    register_plugins(app)
    register_template_context(app)
    # for  development
    register_shell_context(app)
    register_commands(app)
    # register blueprints
    register_blueprints(app)
    return app


def register_blueprints(app):
    from myblog.blueprints.main import main_bp
    from myblog.blueprints.admin import admin_bp
    from myblog.blueprints.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix = '/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_plugins(app):
    db.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app,db)



def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        from myblog.models import Category, Tag, Post, Admin, Comment
        return dict(db=db,  Post=Post, Category=Category, Tag=Tag, Admin=Admin, Comment=Comment)


def bootstrap_is_hidden_field(field):
    return isinstance(field, HiddenField)


def register_template_context(app):

    @app.context_processor
    def make_template_context():
        from myblog.models import Category, Tag, Post, Admin
        categories = Category.query.order_by(Category.name).all()
        tags = Tag.query.order_by(Tag.name).all()
        admin = Admin.query.first()
        return dict(categories=categories, tags=tags, admin=admin)


def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html',description=e.description), 400



def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        from myblog.fakes import fake_default
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
        if drop:
            fake_default()

    @app.cli.command()
    @click.option('--category', default=5, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--tag', default=10, help='Quantity of comments, default is 500.')
    @click.option('--comment', default=200, help='Quantity of comments, default is 500.')
    def forge(category, post, tag, comment):
        """Generate fake data."""
        from myblog.fakes import  fake_categories, fake_posts, fake_tags, fake_comments, fake_default

        db.drop_all()
        db.create_all()
        fake_default()
        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating Tags...')
        fake_tags(tag)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        fake_comments(comment)

        click.echo('Done.')

    @app.cli.command()
    @click.option('--username', default='admin')
    @click.option('--password', default='admin')
    def setadmin(username,password):
        from sqlalchemy.exc import IntegrityError

        from myblog.models import Admin
        account = Admin(username=username, password=password)
        db.session.add(account)
        db.session.commit()
