from sqlalchemy import Column
from sqlalchemy import Integer, Float
from sqlalchemy import String, Boolean

from app.models.base import db,Base
from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import UserMixin
from app import login_manager

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook

from app.models.gift import Gift
from app.models.wish import Wish

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app
from app.models.drift import Drift 
from app.libs.enums import PendingStatus

from math import floor


class User(UserMixin,Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    _password = Column('password', String(128))

    @property
    def password(self):
        return self._password
        
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self,raw):
        if not self._password:
            return False
        return check_password_hash(self._password,raw)

    def generate_token(self,expiration=600):   # 从token中得到重置密码的用户id ,600秒
        s = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expiration)  # 实例化一个虚拟化器
        return s.dumps({'id': self.id}).decode('utf-8') # s.dumpss({'id': self.id}) 将用户信息写入虚拟化器 数据为bytes类型。
            # decode('utf-8')解码, return 将用户数据返回回去  可以把任意信息存入到token中，并非只有id

    @classmethod
    def reset_password(cls,token,new_password):  # 通过token 得知是哪个用户的新密码
        
        s= Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8')) #相反的过程
        except:
            return False

        uid = data.get('id')

        with db.auto_commit():
            user = User.query.get_or_404(uid)
            user.password = new_password    # 会加密 密码，好好想一下。
        return True     

    @classmethod
    def change_password(cls, new_password):
        #     return False
        # return check_password_hash(self._password,raw)
        

        with db.auto_commit():
            user = User.query.get_or_404(id)
            user.password = password1    # 会加密 密码，好好想一下。  
        return True 




    def can_save_to_list(self,isbn):
        if is_isbn_or_key(isbn) != 'isbn':  # 判断是不是isbn
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)   
        if not yushu_book.first:   # 判断 isbn 是否存在
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不能既是赠送者和索要者

        # 既不在 赠送清单 ，也不在心愿清单 才能 添加

        gifting = Gift.query.filter_by(uid = self.id, isbn = isbn,
                                        launched = False).first()

        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        return not wishing and not gifting

#  鱼豆数量必须大于等于1
#  每索取两本书，必须赠送一本书

    def can_send_drifts(self):
        if self.beans < 1:
            return False
        success_gift_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            uid=self.id, pending=PendingStatus.Success).count()

        return floor(success_receive_count / 2) <= success_gift_count

    # def get_id(self):
        # return self.id

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

    def has_in_gifts(self, isbn):
        return Gift.query.filter_by(uid=self.id, isbn=isbn).first() is not None

    def has_in_wishs(self, isbn):
        return Wish.query.filter_by(uid=self.id, isbn=isbn).first() is not None




@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))



