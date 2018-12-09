#生产环境下  nginx + uwsgi
#因为是调用这个模块，所以if __name__ 下面不会运行，这样就不会启用flask内置服务器
from flask import Flask

__author__ = 'weilai'

app = Flask(__name__) 
app.config.from_object('config')

@app.route('/hello/')
def hello2():
    return 'hello world'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=app.config['DEBUG'],port=1)