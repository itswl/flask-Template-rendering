# coding:utf-8

#Flask核心应用app对象初始化应该放在应用层级app包的 __init__.py
from flask import Flask, make_response
from flask_login import LoginManager
from flask_mail import Mail




login_manager = LoginManager()
mail = Mail()  # 实例化mail  在APP中注册flask-mail 

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting') #载入配置文件
    app.config.from_object('app.secure')
    register_blueprint(app)   # 将蓝图注册到app上

    from app.models.book import db
    # 将db插入app
    db.init_app(app)
    # 创建所有的表
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)  #login 初始化工作
    login_manager.login_view = 'web.login'  #未登录状态下跳转到登录界面
    login_manager.login_message = '请先登录或注册'

    mail.init_app(app)  # 注册插件

    return app


def register_blueprint(app):   # 将蓝图注册到app上
    from app.web.book import web
    app.register_blueprint(web)
