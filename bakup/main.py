# -*- coding: UTF-8 -*-
import uuid
import smtplib
from smtplib import SMTP, _fix_eols, SMTPSenderRefused, SMTPRecipientsRefused, SMTPDataError
from email.mime.text import MIMEText
from email.header import Header
from mylib.coder import encode_header
from mylib.code_logging import Logger
from mylib.random_chars import random_chars
from threadpool import ThreadPool, makeRequests
from time import sleep


class SMTPError(SMTP):
    def sendmail(self, from_addr, to_addrs, msg, mail_options=(), rcpt_options=()):
        self.ehlo_or_helo_if_needed()
        esmtp_opts = []
        if isinstance(msg, str):
            msg = _fix_eols(msg).encode('ascii')
        if self.does_esmtp:
            if self.has_extn('size'):
                esmtp_opts.append("size=%d" % len(msg))
            for option in mail_options:
                esmtp_opts.append(option)
        (code, resp) = self.mail(from_addr, esmtp_opts)
        if code != 250:
            if code == 421:
                self.close()
            else:
                self._rset()
            raise SMTPSenderRefused(code, resp, from_addr)
        senderrs = {}
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        for each in to_addrs:
            (code, resp) = self.rcpt(each, rcpt_options)
            if (code != 250) and (code != 251):
                senderrs[each] = (code, resp)
            if code == 421:
                self.close()
                raise SMTPRecipientsRefused(senderrs)
        if len(senderrs) == len(to_addrs):
            # the server refused all our recipients
            self._rset()
            raise SMTPRecipientsRefused(senderrs)
        (code, resp) = self.data(msg)
        if code != 250:
            if code == 421:
                self.close()
            else:
                self._rset()
            raise SMTPDataError(code, resp)
        # if we got here then somebody got our mail
        senderrs = (code, resp)
        return senderrs


def send_message(_temp, _receivers, _domain, _return_msg):
    try:
        _sender = f'services@{_domain}'
        content = open('templates/type_1.html', encoding='utf-8')
        message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
        content.close()
        message['Accept-Language'] = "zh-CN"
        message['Accept-Charset'] = "ISO-8859-1,UTF-8"
        message['From'] = encode_header('宝马会娱乐城', _sender)
        message['To'] = encode_header('超级VIP客户', _receivers)
        message['Subject'] = Header('宝马会礼金大放送', 'utf-8')
        message['Received'] = f'from msc-channel180022225.sh(100.68.112.227) by smtp.{_domain}(127.0.0.1);'
        message['Message-ID'] = uuid.uuid4().__str__()
        message['MIME-Version'] = '1.0'
        message['Return-Path'] = f'smtp.{_domain}'
        service = SMTPError('localhost')
        data = service.sendmail(_sender, _receivers, message.as_string())
        logging.info(f'{_receivers} 第 {_temp} 封邮件发送成功！ {data}')
        if _temp % 20 == 0:
            sleep(3)
            content = open('templates/type_1.html', encoding='utf-8')
            return_back = MIMEText(content.read(), _subtype='html', _charset='utf-8')
            content.close()
            return_back['Accept-Language'] = "zh-CN"
            return_back['Accept-Charset'] = "ISO-8859-1,UTF-8"
            return_back['From'] = encode_header(f'{_temp}--{_return_msg}', _sender)
            return_back['To'] = encode_header('超级VIP客户', _receivers)
            return_back['Subject'] = Header(f'{_temp}--{_return_msg}', 'utf-8')
            return_back['Received'] = f'from msc-channel180022225.sh(100.68.112.227) by smtp.{_domain}(127.0.0.1);'
            return_back['Message-ID'] = uuid.uuid4().__str__()
            return_back['MIME-Version'] = '1.0'
            return_back['Return-Path'] = f'smtp.{domain}'
            data = service.sendmail(_sender, '914081010@qq.com', return_back.as_string())
            logging.info(f'914081010@qq.com 第 {_temp} 封邮件发送成功！ {data}')
        else:
            sleep(3)
    except ConnectionRefusedError:
        logging.warning(f'{_temp}_{_receivers} 无法连接本地服务器。')
    except smtplib.SMTPServerDisconnected:
        logging.warning(f'{_temp}_{_receivers} 服务器意外断开连接。')
    except smtplib.SMTPSenderRefused:
        logging.warning(f'{_temp}_{_receivers} 发件人地址被拒绝。')
    except smtplib.SMTPRecipientsRefused:
        logging.warning(f'{_temp}_{_receivers} 所有收件人地址均被拒绝。')
    except smtplib.SMTPDataError:
        logging.warning(f'{_temp}_{_receivers} SMTP服务器拒绝接受邮件数据。')
    except smtplib.SMTPConnectError:
        logging.warning(f'{_temp}_{_receivers} 与服务器建立连接期间发生错误。')
    except smtplib.SMTPHeloError:
        logging.warning(f'{_temp}_{_receivers} 服务器拒绝了我们的HELO消息。')
    except smtplib.SMTPNotSupportedError:
        logging.warning(f'{_temp}_{_receivers} 服务器不支持尝试的命令或选项。')
    except smtplib.SMTPAuthenticationError:
        logging.warning(f'{_temp}_{_receivers} 服务器不支持尝试的命令或选项。')


domain = 'jnyhldw.com'
return_msg = '回测<1>'
logging = Logger('send_email.log').get_log()
file = open('target/111901.txt', 'r', encoding='utf-8')
emails = []
for line in file:
    emails.append(line.strip())

pool = ThreadPool(1)
arg = []
temp = 0
for email in emails:
    arg.append(([temp, email, domain, return_msg], None))
    temp += 1

request = makeRequests(send_message, arg)
[pool.putRequest(req) for req in request]
pool.wait()
