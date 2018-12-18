from flask_sqlalchemy import SQLAlchemy as  _SQLAlchemy,BaseQuery
from sqlalchemy import SmallInteger, Column
from sqlalchemy import Integer, String
from datetime import datetime
from contextlib import contextmanager

__author__ = 'weilai'

class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

class Query(BaseQuery):

    def filter_by(self, **kwargs):  # **kwargs 表示字典
        if 'status' not in kwargs:  # 取字典所有键的集合
            kwargs['status'] = 1  # 完成自己的filter逻辑
        return super(Query, self).filter_by(**kwargs)  # 继承


db = SQLAlchemy(query_class=Query)  # 替换


# db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time',Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict): # form.data b
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
            