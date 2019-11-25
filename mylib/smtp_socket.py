#! /usr/bin/env python3
import socket
import dns.resolver
import dkim
from smtplib import SMTP
from base64 import b64encode
from email.mime.text import MIMEText

__all__ = ["SMTPException", "SMTPReplyError", "SMTPServerDisconnected", "SMTPSocket"]


class SMTPException(OSError):
    """base exception 基础异常类"""


class SMTPReplyError(SMTPException):
    """reply message error 返回消息异常"""


class SMTPServerDisconnected(SMTPException):
    """disconnection error 连接失败"""


SMTP_PORT = 25
CRLF = "\r\n"
bCRLF = b"\r\n"
_MAXLINE = 8192     # more than 8 times larger than RFC 821, 4.5.3


class SMTPSocket:
    debuglevel = 0

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.service = object
        self.client = object
        self.domain = object

    def send_mail(self, sender, receivers, message, dkim_key=None, dkim_selector=None, dkim_domain=None):
        # type: (str, str, MIMEText, str, str, str) -> (bool, int, str)
        """
        :param sender :
        :param receivers:
        :param message:
        :param dkim_key:
        :param dkim_selector:
        :param dkim_domain:
        :return:
        """
        try:
            temp_data = str(receivers).split('@')
            self.domain = temp_data[1]
            temp_data = str(sender).split('@')
            self.client = temp_data[1]
            self.socket_connect()
            self.helo()
            self.ehlo()
            self.mail_from(sender)
            code, msg = self.mail_rcpt(receivers)
            if code != 250:
                return False, code, msg
            status, code, msg = self.send_data(message, dkim_key, dkim_selector, dkim_domain)
            return status, code, msg
        except SMTPException:
            print('error')
            return False, 0, 'nothing !'

    def socket_connect(self):
        preference, exchange, recode = self.query_mx()
        self.service = exchange
        if self.debuglevel > 0:
            print(f'> Connect: {self.service}')
        self.socket.connect((self.service, SMTP_PORT))
        code, msg = self.get_reply()
        if code != 220:
            self.socket_close()
            raise SMTPServerDisconnected(msg)
        return

    def query_mx(self):
        mx = dns.resolver.query(self.domain, 'MX')
        preference = 0
        exchange = ''
        recode = []
        for i in mx:
            if int(i.preference) > preference:
                recode.append({i.preference, i.exchange})
                preference = i.preference
                exchange = str(i.exchange).strip('.')
        return preference, exchange, recode

    def ehlo(self):
        request = f'EHLO {self.client}{CRLF}'
        if self.debuglevel > 0:
            print(f'> EHLO {self.client}')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == -1 and len(msg) == 0:
            self.socket_close()
            raise SMTPServerDisconnected
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

    def helo(self):
        request = f'HELO {self.service}{CRLF}'
        if self.debuglevel > 0:
            print(f'> HELO {self.service}')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == -1 and len(msg) == 0:
            self.socket_close()
            raise SMTPServerDisconnected
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

    def mail_from(self, sender):
        request = f'MAIL FROM:<{sender}>{CRLF}'
        if self.debuglevel > 0:
            print(f'> MAIL FROM:<{sender}>')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

    def mail_rcpt(self, receivers):
        request = f'RCPT TO:<{receivers}>{CRLF}'
        if self.debuglevel > 0:
            print(f'> RCPT TO:<{receivers}>')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            return code, msg

    def send_data(self, message, dkim_key=None, dkim_selector=None, dkim_domain=None):
        request = f'DATA{CRLF}'
        if self.debuglevel > 0:
            print('> DATA string')
        self.socket.sendall(request.encode('utf-8'))
        code, msg = self.get_reply()
        if code == 354:
            if dkim_key:
                with open(dkim_key) as fh:
                    dkim_key = fh.read()
                    signature = dkim.sign(
                        message=message.as_bytes(),
                        selector=bytes(dkim_selector, encoding='utf-8'),
                        domain=bytes(dkim_domain, encoding='utf-8'),
                        privkey=bytes(dkim_key, encoding='utf-8'),
                    )
                    message['DKIM-Signature'] = bytes.decode(signature.lstrip(b"DKIM-Signature: "))
            self.socket.send(message.as_bytes() + b'\r\n.\r\n')
            code, msg = self.get_reply()
            if code == 250:
                self.socket_close()
                return True, code, msg
            else:
                self.socket_close()
                return False, code, msg
        else:
            self.socket_close()
            return False, code, msg

    def socket_close(self):
        request = f'QUIT{CRLF}'
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        self.socket.close()
        if code == 221:
            return code, msg
        else:
            return -1, ''

    def get_reply(self):
        msg = self.socket.recv(4096)
        if self.debuglevel > 0:
            data = str(msg, encoding='utf-8').split('\r\n')
            for line in data:
                print(f'< {line}')
        if len(msg) > 0:
            data = str(msg, encoding='utf-8').split('\r\n')
            for line in data:
                if line[3:4] == ' ':
                    temp_data = line.split(' ')
                    message = temp_data[1]
                    code = temp_data[0]
                    return int(code), message
            print(data)
            raise SMTPReplyError
        else:
            raise SMTPReplyError
