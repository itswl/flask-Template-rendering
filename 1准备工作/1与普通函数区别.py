from flask import Flask,make_response #创建response对象

__author__ = 'weilai'

#普通函数的return
def hello1():
    return 'hello weilai'

    #视图函数不仅仅返回字符串，还返回  等
    #status code 200,404,301
    #content-type http headers
    #content-type = text/html (默认情况)

    #本质上返回的  Response对象

app = Flask(__name__)
app.config.from_object('config')

@app.route('/hello')
def hello():
    headers = {
        'content-type':'text/plain',   #把它当作普通字符串
        'location': 'https://www.baidu.com'  # 301重定向
        #'content-type': 'application/json'  #json字符串 #下面response就返回的json字符串
    }
    #response = make_response('<html><html>',301)  #301是状态码，只是一个标识，不会影响内容
    #response.headers = headers
    #return response
    return '<html><html>',301,headers #上面3行也可以这样简写

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=app.config['DEBUG'],port=1)
