# coding:utf-8

#from flask import Blueprint
#蓝图的初始化，应该放在对应蓝图层级web包的__init__.py




# 在这里导入不同文件，完成视图函数的注册
from app.web import book 
from app.web import auth
from app.web import drift 
from app.web import gift 
from app.web import main 
from app.web import wish 
# from app.web import user 