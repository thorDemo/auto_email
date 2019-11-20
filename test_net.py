import socket
from email.mime.text import MIMEText
from smtplib import SMTP, _fix_eols, SMTPSenderRefused, SMTPRecipientsRefused, SMTPDataError
from mylib.coder import encode_header
from email.header import Header
import uuid


true_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
true_socket.bind(('104.164.90.157', 0))


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


_return_msg = '回测<test>'
_sender = 'service@abs114.com'
_receivers = '914081010@qq.com'
_domain = 'abs114.com'
_temp = 1
service = SMTPError('104.164.74.244')
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
return_back['Return-Path'] = f'smtp.{_domain}'
data = service.sendmail(_sender, _receivers, return_back.as_string())
print(data)
