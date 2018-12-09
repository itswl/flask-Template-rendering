from .blueprint import web

from flask_login import login_required,current_user  # (得到当前登录用户)
from flask import render_template, request, redirect, url_for, flash

from flask import current_app 

from app.models.gift import Gift

from app.models.base import db

from app.view_models.trade import MyTrade
from app.libs.enums import PendingStatus

from app.models.drift import Drift





__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrade(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):   # current_user 是 user 实例化后的模型
#         # try:      # 事务与回滚
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id

            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']  # 每次上传赠送鱼豆

            db.session.add(gift)
            db.session.add(current_user)
        #     db.session.commit()   # 建议使用过 commit()都用回滚
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash("这本书以添加进您的赠送清单或已经存在于您的心愿清单，请不要重复添加")
    return redirect(url_for('web.book_detail',isbn = isbn))

@web.route('/gifts/<gid>/redraw')  # 撤销礼物
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()

    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            gift.delete()
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']

    return redirect(url_for('web.my_gifts'))





