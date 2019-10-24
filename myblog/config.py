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


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xielei:1234567890@127.0.0.1:3306/myblog'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
