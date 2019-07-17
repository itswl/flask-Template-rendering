# coding:utf-8
#DEBUG默认为false
DEBUG = True   #配置文件全大写，因为小写的找不到
HOST = '0.0.0.0'
PORT = 2333

SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:password@localhost:3306/fisher"

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '***REDACTED***'


# email配置
MAIL_SERVER = 'smtp-mail.outlook.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'imwl@live.com'
# QQ邮箱->设置->账户->[POP3...]->生成授权码->发送短信->获取授权码
MAIL_PASSWORD = '********'
