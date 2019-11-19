# -*- coding: UTF-8 -*-
import uuid
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'serivces@jnyhldw.com'
subject = '宝马会礼金大放送'
receivers = [
    # '914060505@qq.com',
    # '914030606@qq.com',
    # '914820606@qq.com',
    '914081010@qq.com',
]
content = open('templates/type_1.html', encoding='utf-8')
message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
message['Subject'] = Header(subject, 'utf-8')

try:
    service = smtplib.SMTP('localhost')
    service.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
