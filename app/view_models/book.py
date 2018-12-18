# class BookViewModel:

#     @classmethod
#     def package_single(cls, data, keyword):
#         returned = {
#             'book': [],
#             'keyword': keyword,
#             'total': 0
#         }
#         if data:
#             returned['total'] = 1
#             returned['book'] = [BookViewModel.__cut_book_data(data)]
#         return returned

#     @classmethod
#     def package_collection(cls, data, keyword):
#         returned = {
#             'book': [],
#             'keyword': keyword,
#             'total': 0
#         }
#         if data:
#             returned['total'] = data['total'],
#             returned['book'] = [BookViewModel.__cut_book_data(book) for book in data["books"]]
#         return returned

#     @classmethod
#     def __cut_book_data(cls, data):
#         book = {
#             'title': data['title'],
#             'publisher': data['publisher'],
#             'pages': data['pages'] or '',
#             'author': '、'.join(data['author']),
#             'price': data['price'] or '',
#             'summary': data['summary'] or '',
#             'image': data['image']
#         }
#         return book


class BookViewModel:


# 描述特征  (类变量，实例变量)
# 行为（方法）

    # def __init__(self, data):
    #     self.title = data['title']
    #     self.author = '、'.join(data['author'])
    #     self.binding = data['binding'] if data['binding'] else ''
    #     self.publisher = data['publisher']
    #     self.image = data['image']
    #     self.price = '￥' + data['price'] if data['price'] else '' #data['price']
    #     self.isbn = data['isbn']
    #     self.pubdate = data['pubdate'] if data['pubdate'] else ''
    #     self.summary = data['summary'] if data['summary'] else ''
    #     self.pages = data['pages'] if data['pages'] else ''

    def __init__(self, data):
        self.title = data['title']
        self.author = '、'.join(data['author'])
        self.binding = data['binding']
        self.publisher = data['publisher']
        self.image = data['image']
        # self.price = '￥' + data['price']  # 因为价格可能为NONE,str不能和NONE相加，会报错。
        self.price = '￥' + data['price'] if data['price'] else ''

        self.isbn = data['isbn']
        self.pubdate = data['pubdate']
        summary = data['summary']
        self.summary = summary if len(summary) <= 1000 else summary[:1000]
        self.pages = data['pages'].replace('页', '')

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return ' / '.join(intros)


class BookCollection:

    def __init__(self):
        self.keyword = ''
        self.total = 0
        self.books = []

    def fill(self, yushu_book, keyword):
        self.keyword = keyword
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]


class _BookViewModel:

    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'book': [],
            'keyword': keyword,
            'total': 0
        }
        if data:
            returned['total'] = 1
            returned['book'] = [_BookViewModel.__cut_book_data(data)]

        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'book': [],
            'keyword': keyword,
            'total': 0
        }
        if data:
            returned['total'] = data['total'],
            returned['book'] = [_BookViewModel.__cut_book_data(book) for book in data["books"]]

        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'],
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'],
            'image': data['image']
        }
        return book