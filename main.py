# -*-coding:utf-8-*-
from mylib.smtp_socket import SMTPSocket
import uuid
from email.mime.text import MIMEText
from email.header import Header
from mylib.coder import encode_header
from mylib.code_logging import Logger
from mylib.tools import rand_from, rand_to, rand_title
import time


file_name = '111901.txt'
service_name = 'localhost<0>'
delay_time = 5          # 初始延时
delay = 3               # 失败延时


delay_temp = delay_time
emails = open(f'target/{file_name}', 'r')
temp = 0
logging = Logger('send_email.log').get_log()
last_email = open(f'target/last.txt', 'r').readline().strip()
flag = True
for line in emails:
    if line.strip() != last_email and flag:
        continue
    flag = False
    if line.strip() == last_email:
        logging.warning(f'>>{last_email}<<最后提交邮箱 跳过！')
        continue

    if temp % 20 == 0:
        _receivers = '914081010@qq.com'
        _domain = 'bmw1984.com'
        _sender = f'service@{_domain}'
        content = open('templates/type_1.html', encoding='utf-8')
        message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
        content.close()
        message['Accept-Language'] = "zh-CN"
        message['Accept-Charset'] = "ISO-8859-1,UTF-8"
        message['From'] = encode_header(rand_from(), _sender)
        message['To'] = encode_header(rand_to(), _receivers)
        message['Subject'] = Header(f'{service_name} renter:<{temp}>', 'utf-8')
        message['Received'] = f'from msc-channel180022225.sh(128.14.154.138) by mail.{_domain}(127.0.0.1);'
        message['Message-ID'] = uuid.uuid4().__str__()
        message['MIME-Version'] = '1.0'
        message['Return-Path'] = f'mail.{_domain}'
        service = SMTPSocket()
        dkim_key = 'conf/rsaky.pem'
        dkim_selector = 's1'
        dkim_domain = 'bmw1984.com'
        status, code, msg = service.send_mail(_sender, _receivers, message, logging, dkim_key, dkim_selector, dkim_domain)
        if code == 250:
            delay_time = delay_temp
            logging.info(f'{_receivers} 邮件发送成功！延时{delay_time} {temp, status, code, msg}')
        else:
            delay_time += delay
            logging.warning(f'{_receivers} 邮件发送失败！延时{delay_time} {temp, status, code, msg}')
        temp += 1
        time.sleep(delay_time)

    _domain = 'bmw1984.com'
    _receivers = line.strip()
    _sender = f'service@{_domain}'
    content = open('templates/type_1.html', encoding='utf-8')
    message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
    content.close()
    message['Accept-Language'] = "zh-CN"
    message['Accept-Charset'] = "ISO-8859-1,UTF-8"
    message['From'] = encode_header(rand_from(), _sender)
    message['To'] = encode_header(rand_to(), _receivers)
    message['Subject'] = Header(rand_title(), 'utf-8')
    message['Received'] = f'from msc-channel180022225.sh(128.14.154.138) by mail.{_domain}(127.0.0.1);'
    message['Message-ID'] = uuid.uuid4().__str__()
    message['MIME-Version'] = '1.0'
    message['Return-Path'] = f'mail.{_domain}'
    service = SMTPSocket()
    dkim_key = 'conf/rsaky.pem'
    dkim_selector = 's1'
    dkim_domain = 'bmw1984.com'
    status, code, msg = service.send_mail(_sender, _receivers, message, logging, dkim_key, dkim_selector, dkim_domain)
    if code == 250:
        delay_time = delay_temp
        logging.info(f'{_receivers} 邮件发送成功！延时{delay_time} {temp, status, code, msg}')
        file = open('target/last.txt', 'w')
        file.write(_receivers)
        file.close()
    else:
        delay_time += delay
        logging.warning(f'{_receivers} 邮件发送失败！延时{delay_time} {temp, status, code, msg}')
        file = open('target/last.txt', 'w')
        file.write(_receivers)
        file.close()
    temp += 1
    time.sleep(5)

