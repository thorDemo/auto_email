# -*-coding:utf-8-*-
from mylib.smtp_socket import SMTPSocket
import uuid
from email.mime.text import MIMEText
from email.header import Header
from mylib.coder import encode_header
from mylib.code_logging import Logger
import time


emails = open('target/111901.txt')
temp = 0
for line in emails:
    if temp % 20 == 0:
        _receivers = '914081010@qq.com'
        _domain = 'bmw1984.com'
        logging = Logger('send_email.log').get_log()
        _sender = f'service@{_domain}'
        content = open('templates/type_1.html', encoding='utf-8')
        message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
        content.close()
        message['Accept-Language'] = "zh-CN"
        message['Accept-Charset'] = "ISO-8859-1,UTF-8"
        message['From'] = encode_header('宝马会娱乐城', _sender)
        message['To'] = encode_header('超级VIP客户', _receivers)
        message['Subject'] = Header(f'service<1> renter:<{temp}>', 'utf-8')
        message['Received'] = f'from msc-channel180022225.sh(128.14.154.138) by mail.{_domain}(127.0.0.1);'
        message['Message-ID'] = uuid.uuid4().__str__()
        message['MIME-Version'] = '1.0'
        message['Return-Path'] = f'mail.{_domain}'
        service = SMTPSocket()
        dkim_key = 'conf/rsaky.pem'
        dkim_selector = 's1'
        dkim_domain = 'bmw1984.com'
        status, code, msg = service.send_mail(_sender, _receivers, message, dkim_key, dkim_selector, dkim_domain)
        if code == 250:
            logging.info(f'{_receivers} 邮件发送成功！ {status, code, msg}')
        else:
            logging.warning(f'{_receivers} 邮件发送失败！ {status, code, msg}')
        temp += 1
        time.sleep(4)
    else:
        _domain = 'bmw1984.com'
        _receivers = line.strip()
        logging = Logger('send_email.log').get_log()
        _sender = f'service@{_domain}'
        content = open('templates/type_2.html', encoding='utf-8')
        message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
        content.close()
        message['Accept-Language'] = "zh-CN"
        message['Accept-Charset'] = "ISO-8859-1,UTF-8"
        message['From'] = encode_header('宝马会娱乐城', _sender)
        message['To'] = encode_header('超级VIP客户', _receivers)
        message['Subject'] = Header('宝马会礼金大放送', 'utf-8')
        message['Received'] = f'from msc-channel180022225.sh(128.14.154.138) by mail.{_domain}(127.0.0.1);'
        message['Message-ID'] = uuid.uuid4().__str__()
        message['MIME-Version'] = '1.0'
        message['Return-Path'] = f'mail.{_domain}'
        service = SMTPSocket()
        dkim_key = 'conf/rsaky.pem'
        dkim_selector = 's1'
        dkim_domain = 'bmw1984.com'
        status, code, msg = service.send_mail(_sender, _receivers, message, dkim_key, dkim_selector, dkim_domain)
        if code == 250:
            logging.info(f'{_receivers} 邮件发送成功！ {status, code, msg}')
        else:
            logging.warning(f'{_receivers} 邮件发送失败！ {status, code, msg}')
        temp += 1
        time.sleep(4)
