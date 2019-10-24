import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'wPCaYfo1TbEtF2uSnA9m0w')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYBLOG_POST_PER_PAGE = 10
    MYBLOG_COMMENT_PER_PAGE = 10
    MYBLOG_EMAIL = '761018513@qq.com'



class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    DEBUG = True
    MYBLOG_ABOUT_ME = """
#### 前端
- [bootstrap](https://getbootstrap.com/)
- [font-awesome](http://www.fontawesome.com.cn/)
- [前端模版1](https://github.com/BlackrockDigital/startbootstrap-blog-post)
- [前端模版2](https://github.com/BlackrockDigital/startbootstrap-blog-home)
#### 后端
- [flask](https://github.com/pallets/flask) 作为wsgi框架
- [gunicorn](https://gunicorn.org/) 作为wsgi服务器
- [nginx](https://www.nginx.com/) 作为反向代理
        """


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xielei:1234567890@127.0.0.1:3306/myblog'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MYBLOG_ABOUT_ME = """
#### 前端
- [bootstrap](https://getbootstrap.com/)
- [font-awesome](http://www.fontawesome.com.cn/)
- [前端模版1](https://github.com/BlackrockDigital/startbootstrap-blog-post)
- [前端模版2](https://github.com/BlackrockDigital/startbootstrap-blog-home)
#### 后端
- [flask](https://github.com/pallets/flask) 作为wsgi框架
- [gunicorn](https://gunicorn.org/) 作为wsgi服务器
- [nginx](https://www.nginx.com/) 作为反向代理
    """

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
