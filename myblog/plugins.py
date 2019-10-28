from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import html
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


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            lang = 'bash'
            #return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound as e:
            print('lang {} not found from lexer'.format(lang))
            return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
        formatter = html.HtmlFormatter(cssclass='codehilite')
        return highlight(code, lexer, formatter)

renderer = HighlightRenderer()
mistune_md = mistune.Markdown(renderer=renderer)
#mistune_md = mistune.Markdown()
#print(mistune_md('```python\nassert 1 == 1\n```'))
