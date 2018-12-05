# coding:utf-8

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from flask import jsonify
# from flask import Blueprint  转移到__inti__中
from .blueprint import web  #实例化蓝图后，导入蓝图，注册视图函数

from flask import request  # 改造后 

from app.forms.book import SearchForm  #使用WTForms 
from app.view_models.book import BookViewModel,BookCollection

import json

from flask import render_template, flash
# # web = Blueprint('web', __name__)  # 'web'模块名，__name__蓝图所在包或者模块 # 转移到 app.web.blueprint中


# # @web.route("/book/search/<q>/<page>")  
# # def search(q, page):
#     # '''
#     #     q: 普通关键字  isbn 
#     #     page
#     # '''
#     # isbn_or_key = 'key'
#     # if len(q) == 13 and q.isdigit():
#     #     isbn_or_key = 'isbn'
#     # short_q = q.replace('-','')
#     # if '-' in q and len(short_q) == 10 and short_q.isdigit:
#     #     isbn_or_key ='isbn'
#     # 将以上代码封装为一个函数然后调用比较合理
#     isbn_or_key = is_isbn_or_key(q)
#     if isbn_or_key == 'isbn':
#         result = YuShuBook.search_by_isbn(q)
#     else:
#         result = YuShuBook.search_by_keyword(q)
    
#     # dict 序列化
#     # return json.dumps(result),200,{'content-type':'application/json'}  #python自带
#     return jsonify(result)


# 改造一下

# @web.route('/book/search/')
# def search():
#     """
#     搜索书籍路由
#     :param q: 关键字 OR isbn
#     :param page: 页码
#     """
#     q = request.args['q']
#     page = request.args['page']
#     isbn_or_key = is_isbn_or_key(q)
#     if isbn_or_key == 'isbn':
#         result = YuShuBook.search_by_isbn(q)
#     else:
#         result = YuShuBook.search_by_keyword(q)
#     return jsonify(result)


# 使用WTForms book.py
@web.route("/book/search")
def search():
    """
    搜索书籍路由
    """
    # 实例化我们自定义的SearchForm，需要传入一个字典作为要校验的参数
    form = SearchForm(request.args)
    # validate()方法返回True/False来标示是否校验通过
    books = BookCollection()
    # if not form.validate():
    #     # errors为错误信息提示（上面定义的message）
    #     flash("搜索的关键字不符合要求，请重新输入关键字")
    #     return render_template('search_result.html', books=books)
    # 从form中获取校验后的参数，不从request里拿，因为我们可能会对数据进行预处理或者默认值的给定
    q = form.q.data.strip()
    page = form.page.data
    isbn_or_key = is_isbn_or_key(q)
    yushu_book = YuShuBook()
    if form.validate():
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            books.fill(yushu_book,q)
        # result = YuShuBook.search_by_isbn(q)
        # result = BookViewModel.package_single(result,q) 
        else:
            yushu_book.search_by_key(q,page)        
        # result = YuShuBook.search_by_keyword(q,page)
        # result = BookViewModel.package_collection(result,q)
    # return jsonify(result)
            books.fill(yushu_book,q)
    else:
        flash("搜索的关键字不符合要求，请重新输入关键字")

    # return jsonify(books)  # TypeError: Object of type BookCollection is not JSON serializable
    # return json.dumps(books, default=lambda o: o.__dict__)
    return render_template('search_result.html', books=books)
# 遇到的坑   base.html 关于user注释掉。不能用ctrl +/  ，所以报错 'current_user' is undefined

@web.route("/book/<isbn>/detail")
def book_detail(isbn):
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    return render_template("book_detail.html", book=book, wishes=[], gifts=[])


