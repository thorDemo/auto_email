import socket
import ssl
import base64
import time
import os
import random


# Exception classes used by this module.
class SMTPException(OSError):
    """Base class for all exceptions raised by this module."""


class SMTPServerDisconnected(SMTPException):
    """Not connected to any SMTP server.

    This exception is raised when the server unexpectedly disconnects,
    or when an attempt is made to use the SMTP instance before
    connecting it to a server.
    """


class ProxySMTP:

    def __init__(self, proxy_ip):
        self._true_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._true_socket.bind((proxy_ip, 0))
        self.command_encoding = 'ascii'
        self.__ssl_client_Socket = object

    def socket_connect(self):
        self.__ssl_client_Socket = ssl.wrap_socket(
            self._true_socket,
            cert_reqs=ssl.CERT_NONE,
            ssl_version=ssl.PROTOCOL_SSLv23
        )
        self.__ssl_client_Socket.connect(('smtp.qq.com', 465))
        res = self.__ssl_client_Socket.recv(1024).decode('utf-8')
        print(res)

    def send_mail(self, _sender, _receivers):
        self.socket_connect()

    def hello(self):
        # self.__ssl_client_Socket.send(b'HELO qq.com\r\n')
        # res = self._true_socket.recv(1024)
        # if res:
        #     data = str(res, encoding='utf-8')
        #     data = data.split('\r\n')
        #     for line in data:
        #         if 'title' in line:
        #             print(line)
        # else:
        #     print(f"visit {0} error")
        pass

    def send(self, s):
        """Send `s' to the server."""
        if hasattr(self, 'sock') and self.sock:
            if isinstance(s, str):
                # send is used by the 'data' command, where command_encoding
                # should not be used, but 'data' needs to convert the string to
                # binary itself anyway, so that's not a problem.
                s = s.encode(self.command_encoding)
            try:
                self.sock.sendall(s)
            except OSError:
                self._true_socket.close()
                raise SMTPServerDisconnected('Server not connected')
        else:
            raise SMTPServerDisconnected('please run connect() first')


ps = ProxySMTP('104.164.74.244')
ps.send_mail('1935940593@qq.com', '')
