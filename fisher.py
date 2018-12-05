# coding:utf-8
from app import create_app


__author__ = 'weilai'

app = create_app()


@app.route('/')
def index():
    return 'Hello'


if __name__ == '__main__':
    app.run(host=app.config["HOST"], debug=app.config["DEBUG"], port=app.config["PORT"])
