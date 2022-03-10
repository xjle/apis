"""
    常用工具类
"""
from flask_mail import Message
from apps.ext import mail


def send_mail(subject, recipient, body):
    """
    :param subject: 标题
    :param recipient:  接受方
    :param body: 内容
    :return:
    """
    msg = Message(subject=subject, recipients=[recipient], body=body)
    try:
        mail.send(msg)
        return True
    except EnvironmentError as e:
        return False
