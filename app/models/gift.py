from app.models.base import db,Base# 一定要导入BASE,不然获取不到uid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship
from flask import current_app  

from app.spider.yushu_book import YuShuBook

# from collections import namedtuple  #  快速定义对象

__author__ = 'weilai'

class Gift(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    # relationships表示管理关系
    user = relationship('User')
    # ForeignKey定义外键约束
    uid = Column(Integer, ForeignKey('user.id'))
    # 书籍我们记录isbn编号，因为书籍信息是从网络获取的
    isbn = Column(String(15),nullable=True)
    # 是否已经赠送出去
    launched = Column(Boolean, default=False)
  
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first



    # @classmethod
    # def recent(cls):
    #     # 链式调用 主体是Query ，遇到all(),first()就会终止生成一条sql
    #     # 建造者模式
    #     # select distinct * from gift group by isbn order by create_time limit 30
    #     recent_gift = Gift.query.filter_by(
    #         launched=False).group_by(
    #         Gift.isbn
    #         ).order_by(desc(          # desc 表示倒序排列
    #         Gift.create_time)).limit(
    #         current_app.config['RECENT_BOOK_COUNT']).distinct().all()
    #     return recent_gift

    @classmethod
    def recent(cls):
        # select distinct * from gift group by isbn order by create_time limit 30
        recent_gifts = Gift.query \
            .filter_by(launched=False) \
            .order_by(Gift.create_time) \
            .limit(30) \
            .distinct().all()
        return recent_gifts
    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query \
            .filter_by(uid=uid, launched=False) \
            .order_by(desc(Gift.create_time)) \
            .all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 根据传入的一组isbn编号，到Wish表中计算出某个礼物的Wish心愿数量
        # select count(id),isbn from wish
        # where launched = false and isbn in ('','') and status =1 group by isbn
        from app.models.wish import Wish

        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        # 不要将tuple返回到外部，应该返回有意义的字典或者对象
        count_list = [{'count': w[0], 'isbn':w[1]} for w in count_list]
        return count_list

    @classmethod
    def get_user_gifts_by_sql(cls, uid):
        sql = 'select a.id,a.isbn,count(b.id)' \
              'from gift a left join wish b on a.isbn = b.isbn ' \
              'where b.uid = %s and a.launched = 0 and b.launched = 0 ' \
              'and a.status = 1 and b.status = 1 ' \
              'group by a.id,a.isbn order by a.create_time desc'.replace('%s', str(uid))
        gifts = db.session.execute(sql)
        gifts = [{'id': line[0], 'isbn': line[1], 'count':line[2]} for line in gifts]
        return gifts

    @classmethod
    def get_user_gifts_by_orm(cls, uid):
        from app.models.wish import Wish

        gifts = db.session\
            .query(Gift.id, Gift.isbn, func.count(Wish.id))\
            .outerjoin(Wish, Wish.isbn == Gift.isbn)\
            .filter(
                Gift.launched == False,
                Wish.launched == False,
                Gift.status == 1,
                Wish.status == 1,
                Gift.uid == uid)\
            .order_by(desc(Gift.create_time))\
            .all()
        gifts = [{'gift': gift[0], 'count':gift[1]} for gift in gifts]
        return gifts

#  自己不能够向自己索要数据

    def is_yourself_gift(self, uid):
        return uid == self.uid

