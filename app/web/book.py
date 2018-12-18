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

from app.models.gift import Gift
from app.models.wish import Wish
from app.models.book import Book
from app.view_models.trade import TradeInfo

from flask_login import current_user
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
            Book.insert_into_sql(books.books)
            # print(11111, books.books)
            # for b in books.books:
            #     print('title', b.title)
            #     print('author', b.author)
        # result = YuShuBook.search_by_isbn(q)
        # result = BookViewModel.package_single(result,q) 
        else:
            yushu_book.search_by_key(q,page)        
        # result = YuShuBook.search_by_keyword(q,page)
        # result = BookViewModel.package_collection(result,q)
    # return jsonify(result)
            books.fill(yushu_book,q)
            Book.insert_into_sql(books.books)
    else:
        flash("搜索的关键字不符合要求，请重新输入关键字")

    # return jsonify(books)  # TypeError: Object of type BookCollection is not JSON serializable
    # return json.dumps(books, default=lambda o: o.__dict__)
    return render_template('search_result.html', books=books)
# 遇到的坑   base.html 关于user注释掉。不能用ctrl +/  ，所以报错 'current_user' is undefined


# @web.route("/book/<isbn>/detail")
# def book_detail(isbn):
#     has_in_gifts = False
#     has_in_wishes = False

#     # 取出每本书的详情
#     yushu_book = YuShuBook()
#     yushu_book.search_by_isbn(isbn)
#     book = BookViewModel(yushu_book.first)

#     # 三种情况的判断
#     if current_user.is_authenticated:
#         print(111, Gift.query.filter_by(uid=1).first())
#         if Gift.query.filter_by(uid=current_user.id).first():
#             has_in_gifts = True
#         if Wish.query.filter_by(uid=current_user.id).first():
#             has_in_wishes = True

#     # 赠书人列表和索要人列表
#     trade_gifts = Gift.query.filter_by(isbn=isbn).all()
#     trade_wishes = Wish.query.filter_by(isbn=isbn).all()



#     return render_template("book_detail.html", book=book,
#                            wishes=trade_wishes, gifts=trade_gifts,
#                            has_in_wishes=has_in_wishes, has_in_gifts=has_in_gifts)

@web.route("/book/<isbn>/detail")
def book_detail(isbn):

    # 取出每本书的详情
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 三种情况的判断
    has_in_gifts = current_user.is_authenticated and current_user.has_in_gifts(isbn)
    has_in_wishes = current_user.is_authenticated and current_user.has_in_wishs(isbn)

    # 赠书人列表和索要人列表
    trade_gifts = Gift.query.filter_by(isbn=isbn).all()
    trade_wishs = Wish.query.filter_by(isbn=isbn).all()

    trade_wishs_model = TradeInfo(trade_wishs)
    trade_gifts_model = TradeInfo(trade_gifts)
    return render_template("book_detail.html", book=book,
                           wishes=trade_wishs_model, gifts=trade_gifts_model,
                           has_in_wishes=has_in_wishes, has_in_gifts=has_in_gifts)
