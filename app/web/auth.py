from .blueprint import web 
from flask import render_template, request, redirect, url_for, flash

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm,ChangePasswordForm

from app.models.base import db, Base

from app.models.user import User

from flask_login import login_user, logout_user, current_user, login_required
from app.libs.email import send_mail

__author__ = '七月'


# @web.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm(request.form)
    # #request.form
    # if request.methods == 'POST' and form.validate():

    # return render_template('auth/register.html',form ={'data' : {}})
    #     form = RegisterForm(request.form)
@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        # db.session.commit()
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)
        # form = RegisterForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     with db.auto_commit():
    #         user = User()
    #         user.set_attrs(form.data)
    #         db.session.add(user)

    #     return redirect(url_for('web.login'))

    # return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)

            next = request.args.get('next')  # 跳转到登陆前的页面
            if not next or not next.startswith('/'):  # 防止重定向攻击
                return redirect(url_for('web.index'))  
            return redirect(next)
        else:
            flash("账号不存在或者密码错误")
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        account_email = form.email.data
        user = User.query.filter_by(email=account_email).first_or_404()  # 避免自己处理用户为空的情况
        send_mail(
            account_email, "重置你的密码", 'email/reset_password.html',
            user=user, token=user.generate_token())
        flash('重置密码邮件已经发送成功，请到邮箱中查收')
        # return redirect(url_for('web.login'))  # 邮件发送成功后，跳转到web.login
    return render_template('auth/forget_password_request.html', form=form)


# 单元测试






@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('您的密码已重置，请使用新密码登录')
            return redirect(url_for('web.login'))
        flash('密码重置失败')
    return render_template('auth/forget_password.html', form = form)

@web.route('/change/password', methods=['GET', 'POST'])
@login_required 
def change_password():
    form = ChangePasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        if current_user.check_password(form.old_password.data):
            current_user.change_password(form.password1.data)
            flash('您的密码已重置，请使用新密码登录')
            return redirect(url_for('web.login'))
        flash('密码更改失败')
    return render_template('auth/change_password.html')


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))

