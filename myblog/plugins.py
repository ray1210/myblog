from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import html




db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    from myblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'


class CustomRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang):
        if not lang:
            lang = 'bash'
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound as e:
            print('lang {} not found from lexer'.format(lang))
            return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
        formatter = html.HtmlFormatter(cssclass='codehilite')
        return highlight(code, lexer, formatter)


renderer = CustomRenderer()
mistune_md = mistune.Markdown(renderer=renderer)
