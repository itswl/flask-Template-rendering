from app.models.base import db,Base

from sqlalchemy import Column, Integer, String




__author__ = 'weilai'


# 继承db.Model
class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=True)
    author = Column(String(300), default="未名")
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    isbn = Column(String(15), nullable=True, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

   
    @classmethod
    def insert_into_sql(cls, books):
        # book model 写入
        import sqlalchemy
        for b in books:
            # print(111111111111, b.pages)
            if Book.query.filter_by(isbn=b.isbn).first():
                        continue
            with db.auto_commit():
                book = Book()
                book.set_attrs(b.__dict__)  # [b1, b2, b3] 
                # 类lishi后的一个对象 b.author b.title
                db.session.add(book)
        # return   
        # for b in books:    # 优化后如上
        #     with db.auto_commit():
        #         try:
        #             if Book.query.filter_by(isbn=b.isbn).first():
        #                 continue
        #             book = Book()
        #             book.title = b.title
        #             book.author = b.author
        #             book.binding =b.binding
        #             book.publisher = b.publisher
        #             book.price = b.price
        #             book.pages = b.pages
        #             book.isbn = b.isbn
        #             book.summary = b.summary
        #             book.image = b.image
        #             db.session.add(book)
        #         except sqlalchemy.exc.DataError:
        #             pass