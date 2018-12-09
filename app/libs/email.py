"""
create by gaowenfeng on 
"""
from threading import Thread

from app import mail
from flask_mail import Message
from flask import current_app, render_template


def send_mail_async(app, msg):
    # App_Context 的栈Local Stack是线程隔离的，在新线程里栈顶为空，需要手动入栈
    with app.app_context():  #  手 动 入 栈
        try:
            mail.send(msg)
        except:
            print('邮件发送失败')


def send_mail(to, subject, template, **kwargs): # to发给谁，subject标题，template模板，
    msg = Message(
        '[鱼书]'+' '+subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[to])
    msg.html = render_template(template, **kwargs)
     # current_app是代理对象，在当前线程下有指向，但是在新开启的线程中就没了，因为LocalProxy是线程
    app = current_app._get_current_object()   # app是真实的核心对象<flask 'app'>,并非代理apps
    thr = Thread(target=send_mail_async, args=[app,msg])
    thr.start()
# 异步发送邮件  线程隔离 
# 因为使用的第三方邮件，发送时间不可控，并且也不需要在页面等待邮件发送成功再
# 执行下一步，所以异步发送邮件
# 平常时，尽量少使用异步