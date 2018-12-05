from app.models.base import db
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

__author__ = "gaowenfeng"

class Gift(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    # relationships表示管理关系
    user = relationship('User')
    # ForeignKey定义外键约束
    uid = Column(Integer, ForeignKey('user.id'))
    # 书籍我们记录isbn编号，因为书籍信息是从网络获取的
    isbn = Column(String(15),nullable=True)
    # 是否已经赠送出去
    launched = Column(Boolean, default=False)