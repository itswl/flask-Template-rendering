# coding:utf-8
#封装  调用请求类

from app.libs.httper import HTTP
from flask import current_app 

# class YuShuBook:
    # isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    # keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    # def search_by_isbn(self,isbn):
    #     url = YushuBook.isbn_url.format(isbn)
    #     #url = self.isbn_url.format(isbn)
    #     result = HTTP.get(url)
    #     #dict
    #     return result
        
    # def search_by_keyword(self,keyword):
    #     url = YushuBook.keyword_url.format(keyword)
    #     result = HTTP.get(url)
    #     return result
    # 没有用到 self 无意义

    # @classmethod
    # def search_by_isbn(cls,isbn):
    #     url = cls.isbn_url.format(isbn)
    #     #url = self.isbn_url.format(isbn)
    #     result = HTTP.get(url)
    #     #dict
    #     return result

    # @classmethod            
    # def search_by_keyword(cls,keyword,page=1):
    #     url = cls.keyword_url.format(keyword,current_app.config['PER_PAGE'],cls.caculate_start(page))
    #     result = HTTP.get(url)
    #     return result

    # @staticmethod
    # def caculate_start(page):
    #     return (page-1) * current_app.config['PER_PAGE']

class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_key(self, q, page=1):
        url = self.keyword_url.format(q, current_app.config["PER_PAGE"],
                                           self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_single(self, data):
        if data:
            self.books = [data]
            self.total = 1

    def __fill_collection(self, data):
        self.books = data['books']
        self.total = data['total']

    def calculate_start(self, page):
        return (page-1) * current_app.config["PER_PAGE"]

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None