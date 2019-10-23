from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from markdown import Markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension



db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
csrf = CSRFProtect()
md = Markdown(extensions=[FencedCodeExtension(), TableExtension(), CodeHiliteExtension()], output_format='html5')

@login_manager.user_loader
def load_user(user_id):
    from myblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
