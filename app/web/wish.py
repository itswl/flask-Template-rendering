from .blueprint import web 
from flask_login import login_required,current_user  # (得到当前登录用户)
from flask import render_template, request, redirect, url_for, flash

from flask import current_app 

from app.models.wish import Wish
from app.models.gift import Gift

from app.view_models.trade import MyTrade

from app.models.base import db

from app.libs.email import send_mail

__author__ = '七月'


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrade(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)



@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):   # current_user 是 user 实例化后的模型
        # try:      # 事务与回滚
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id

            # current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']  # 每次上传赠送鱼豆

            db.session.add(Wish)

        #     db.session.commit()   # 建议使用过 commit()都用回滚
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash("这本书以添加进您的赠送清单或已经存在于您的心愿清单，请不要重复添加")
    return redirect(url_for('web.book_detail',isbn = isbn))



@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    """
        向想要这本书的人发送一封邮件
        注意，这个接口需要做一定的频率限制
        这接口比较适合写成一个ajax接口
    """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_mail(wish.user.email, '有人想送你一本书', 'email/satisify_wish.html', wish=wish,
                   gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()

    with db.auto_commit():
        wish.delete()

    return redirect(url_for('web.my_wish'))