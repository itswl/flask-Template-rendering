
from wtforms import StringField, PasswordField, Form
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from app.models.user import User

__author__ = "weilai"


class EmailForm(Form):
    email = StringField(validators=[
        DataRequired(), Length(8, 64, message='电子邮箱不符合规范')])


class RegisterForm(EmailForm):  #  注册信息
    nickname = StringField('昵称', validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要2个字符，最多10个字符')])

    password = PasswordField('密码', validators=[
        DataRequired(), Length(6, 32, message='密码长度至少6个字符，最多32个字符')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')


class LoginForm(EmailForm):   # 登陆密码
    password = PasswordField('密码', validators=[
        DataRequired(), Length(6, 32)])


class ResetPasswordForm(Form):   # 重置密码 新密码要求
    password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(), Length(6, 30)])


class ChangePasswordForm(ResetPasswordForm):   # 重置密码 新密码要求

    old_password = PasswordField('密码', validators=[
        DataRequired()])

    # def validate_old_password(self, field):
    #     # if User.query.filter_by(password=field.data).first():
    #     #     raise ValidationError('昵称已存在')
    #     # TODO 验证原密码输入正确
    #     return True
