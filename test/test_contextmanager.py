"""
create by gaowenfeng on 
"""

__author__ = 'weilai'
from contextlib import contextmanager


@contextmanager
def book_mark():
    print('《', end='')
    yield
    print('》', end='')


with book_mark():
    print('挪威的森林',end='')

'''
先执行   print('《', end='')
再执行   print('挪威的森林',end='')
最后执行 print('》', end='')
'''
