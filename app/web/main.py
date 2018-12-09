from .blueprint import web 
from flask import render_template, request, redirect, url_for, flash
from  app.models.gift import Gift

from app.view_models.book import BookViewModel

__author__ = '七月'


@web.route('/')
def index():
    recent_gift = Gift.recent()
    books =  [BookViewModel(gift.book) for gift in recent_gift] 
    return render_template('index.html',recent =books)


@web.route('/personal')
def personal_center():
    return render_template('personal.html')
