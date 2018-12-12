# coding:utf-8

from flask import Blueprint

from flask import render_template 

web = Blueprint('web', __name__)  # 实例化蓝图

@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404