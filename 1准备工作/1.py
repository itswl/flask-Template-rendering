'''
1、安装 python 环境
2、检验 python 和 pip 是否安装好（pip是安装python包的工具）
(python到官网上下载安装升级，pip更新命令 python -m pip install --upgrade pip)
3、新建项目文件夹 mkdir fisher
(4、安装virtualenv)(虚拟环境可以隔离不同的版本)

#pipenv是Python官方推荐的包管理工具。可以说，它集成了virtualenv, pip和pyenv三者的功能。
5、安装使用pipnv  (pip install pipenv)(全局安装pipenv) 
(使用pipenv创建一个与项目绑定的虚拟环境。cd fisher 然后pipenv install )
(pipenv shell进入虚拟环境)
6、安装各种包
(例如flask pipenv install flask)

退出虚拟环境 exit 
进入虚拟环境 pipenv shell
卸载包 eg:  pipenv uninstall flask
使用pipenv graph命令可以看到依赖树
'''

'''
开发工具  Pycharm(VScode)  Pycharm 在断点调试和自动重启服务器支持较好
Xampp(MySQL)
Navicat(数据库可视化管理工具)
'''
from flask import Flask

__author__ = 'weilai'

app = Flask(__name__)    #类的实例化
#route装饰器 ： 优雅方便但不够灵活
#route装饰器 ：可以使用Flask应用实例的route装饰器将一个URL规则绑定到 一个视图函数上
#基于类的视图(即插视图),基于函数的视图
#@app.route('/hello')  # 使用 route() 装饰器来告诉 Flask 触发函数的 URL 。 /hello 可以访问
@app.route('/hello/')  #兼容/  把/hello 重定向到/hello/
def hello():

    return 'hello world'

    

#app.run()
# app.run(debug=True)  #开启调试模式，可以显示bug原因，也可以不需要修改后重启服务器，自动重启。

#另一种路由注册方式
#一般都是用route装饰器，但即插视图，必须使用add_url_rule
def hello1():

    return 'hello China'

app.add_url_rule('/hello1',view_func = hello1)



app.run()  #直接运行
app.run(debug=True) #开启调试模式
app.run(host='192.168.2.136',debug=True)  #指定ip地址，仅本机，网卡为192.168.2.136的可访问
app.run(host='0.0.0.0',debug=True) #起它ip地址也可以访问
app.run(host='0.0.0.0',debug=True,port=1)  #改端口







'''端口取值：
一般用到的是1到65535,其中0不使用,1-1023为系统端口,也叫BSD保留端口;
1024-65535为用户端口， 又分为: BSD临时端口(1024-5000)和BSD服务器(非特权)端口(5001-65535).
0-1023: BSD保留端口,也叫系统端口,这些端口只有系统特许的进程才能使用;
1024-5000: BSD临时端口,一般的应用程序使用1024到4999来进行通讯;
5001-65535: BSD服务器(非特权)端口,用来给用户自定义端口.
一般的应用程序就是指系统中的ftp，apache，ssh之类的应用程序。而用户自定义的应用程序就是你自己在系统上开发的应用程序。属于你的东西。操作系统不会把它作为一个通用的功能，集成到系统去。
'''