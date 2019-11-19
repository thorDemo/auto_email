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
message['Accept-Language'] = "zh-CN"
message['Accept-Charset'] = "ISO-8859-1,UTF-8"
message['From'] = '宝马会娱乐城 serivces@jnyhldw.com'
message['To'] = '超级VIP客户 914081010@qq.com'    # 接收者
message['Subject'] = Header(subject, 'utf-8')
message['Received'] = 'from msc-channel180022225.sh(100.68.112.227) by smtp.aliyun-inc.com(127.0.0.1);'
message['Message-ID'] = uuid.uuid4().__str__()
message['MIME-Version'] = '1.0'
message['Return-Path'] = 'smtp.jnyhldw.com'
# print(message)
try:
    service = smtplib.SMTP('localhost')
    service.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print(e)
    print("Error: 无法发送邮件")
