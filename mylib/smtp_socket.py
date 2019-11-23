#! /usr/bin/env python3
import socket
import dkim
from smtplib import SMTP
from base64 import b64encode

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

    def send_mail(self, sender, receivers, message):
        # type: (str, str, str) -> str
        """
        :param sender :
        :param receivers:
        :param message:
        :return:
        """
        try:
            temp_data = str(receivers).split('@')
            self.service = f'smtp.{temp_data[1]}'
            temp_data = str(sender).split('@')
            self.client = temp_data[1]
            print((self.service, SMTP_PORT))
            self.socket.connect((self.service, SMTP_PORT))
            code, msg = self.get_reply()
            if code != 220:
                self.socket_close()
                raise SMTPServerDisconnected(msg)
            self.helo()
            self.ehlo()
            self.mail_from(sender)
            print(2)
            self.mail_rcpt(receivers)
            print(3)
            self.send_data(message)
            print(4)
            return ''
        finally:
            self.socket_close()

    def ehlo(self):
        request = f'EHLO {self.client}{CRLF}'
        print(f'EHLO {self.client}')
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
        print(f'HELO {self.service}')
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
        print(f'MAIL FROM:<{sender}>')
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

    def mail_rcpt(self, receivers):
        request = f'MAIL FROM:<{receivers}>{CRLF}'
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == 250:
            return code, msg
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

    def send_data(self, message_data):
        request = f'DATA{CRLF}'
        self.socket.sendall(str(request).encode('utf-8'))
        code, msg = self.get_reply()
        if code == 354:
            self.socket.sendall(message_data)
            code, msg = self.get_reply()
            if code == 250:
                self.socket_close()
                return code, msg
            else:
                self.socket_close()
                raise SMTPReplyError(code, msg)
        else:
            self.socket_close()
            raise SMTPReplyError(code, msg)

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
                print(line)
        if len(msg) > 0:
            data = str(msg, encoding='utf-8').split('\r\n')
            for line in data:
                if '250 ' in line or '220 ' in line:
                    temp_data = line.split(' ')
                    message = temp_data[1]
                    code = temp_data[0]
                    return int(code), message
        else:
            self.socket_close()
            raise SMTPReplyError

