#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'memgq'

import socket
import ssl
import base64
import time
import os
import random


class SendMail:
    __username=''
    __password=''
    __recipient=''
    msg = b'\r\n'
    endmsg = b'\r\n.\r\n'
    mailserver = ('smtp.qq.com', 465)
    heloCommand = b'HELO qq.com\r\n'
    loginCommand = b'AUTH login\r\n'
    dataCommand = b'DATA\r\n'
    quitCommand = b'QUIT\r\n'
    msgsubject = b'Subject: Test E-mail\r\n'
    msgtype = b"Content-Type: multipart/mixed;boundary='BOUNDARY'\r\n\r\n"
    msgboundary = b'--BOUNDARY\r\n'
    msgmailer = b'X-Mailer:mengqi\'s mailer\r\n'
    msgMIMI = b'MIME-Version:1.0\r\n'
    msgfileType = b"Content-type:application/octet-stream;charset=utf-8\r\n"
    msgfilename = b"Content-Disposition: attachment; filename=''\r\n"
    msgimgtype = b"Content-type:image/gif;\r\n"
    msgimgname = b"Content-Disposition: attachment; filename=''\r\n"
    msgtexthtmltype = b'Content-Type:text/html;\r\n'
    msgimgId = b'Content-ID:<test>\r\n'
    msgimgscr = b'<img src="cid:test">'
    mailcontent = ''
    __clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def login(self):
        """
        输入用户名和授权码登陆QQ邮箱
        """
        print("正在发送登录请求……")
        time.sleep(1)
        self.__sslclientSocket.send(self.loginCommand)
        recv2 = self.__sslclientSocket.recv(1024).decode('utf-8')
        if recv2[:3] !='334':
            print('登录请求发送失败：334 reply not received from server.')
            time.sleep(2)
            print('正在重试……')
            self.login()
        print("登录请求发送成功……")
        self.__username = input("请输入用户名：")
        self.__password = input("请输入授权码：")
        print("正在登录……")
        time.sleep(1)
        username = b'%s\r\n' % base64.b64encode(self.__username.encode('utf-8'))
        self.__sslclientSocket.send(username)
        recv = self.__sslclientSocket.recv(1024).decode('utf-8')
        password = b'%s\r\n' % base64.b64encode(self.__password.encode('utf-8'))
        self.__sslclientSocket.send(password)
        recv = self.__sslclientSocket.recv(1024).decode('utf-8')
        if recv[:3] != '235':
            print('登录失败：账号或密码错误，请使用授权码登录. 235 reply not received from server.',recv)
            time.sleep(2)
            print('正在重试……')
            self.login()
        print("登录成功")
        time.sleep(1)


    def socketconnet(self):
        """
        使用socket套接字连接qq邮箱服务器，并设置ssl验证
        """
        print("正在连接服务器……")
        time.sleep(1)
        self.__sslclientSocket = ssl.wrap_socket(self.__clientSocket, cert_reqs=ssl.CERT_NONE,
                                            ssl_version=ssl.PROTOCOL_SSLv23)
        self.__sslclientSocket.connect(self.mailserver)
        recv = self.__sslclientSocket.recv(1024).decode('utf-8')
        if recv[:3] != '220':
            print('服务器连接失败：220 reply not received from server.')
            time.sleep(2)
            print('正在重试……')
            self.socketconnet()
        print("成功连接服务器……")
        time.sleep(1)
        print("正在请求服务器响应……")
        time.sleep(1)
        self.__sslclientSocket.send(self.heloCommand)
        recv1 = self.__sslclientSocket.recv(1024).decode('utf-8')
        if recv1[:3] != '250':
            print('服务器响应失败：250 replay not received from server')
            time.sleep(2)
            print('正在重试……')
            self.socketconnet()
        print("成功请求服务器响应……")
        time.sleep(1)


    def sender(self):
        mailsenderCommand = b'MAIL FROM:<%s>\r\n' % self.__username.encode('utf-8')
        self.__sslclientSocket.send(mailsenderCommand)

    def recipient(self):
        self.__recipient = input("请输入收件人邮箱：")
        time.sleep(1)
        mailrecipientCommand = b'RCPT TO:<%s>\r\n' % self.__recipient.encode('utf-8')
        self.__sslclientSocket.send(mailrecipientCommand)
        recv = self.__sslclientSocket.recv(1024).decode('utf-8')
        if recv[:3] != '250':
            print("收件人邮箱错误:250 replay not received from server")
            time.sleep(1)
            self.recipient()

    def senddata(self):
        self.__sslclientSocket.send(self.dataCommand)
        recv = self.__sslclientSocket.recv(1024).decode('utf-8')
        if recv[:3] != '354':
            time.sleep(1)
            self.senddata()

    def sendsubject(self):
        subject = input("请输入邮件主题：")
        time.sleep(1)
        self.msgsubject = b'Subject: %s\r\n' % subject.encode('utf-8')
        self.__sslclientSocket.send(self.msgsubject)
        self.__sslclientSocket.send(self.msgmailer)
        self.__sslclientSocket.send(self.msgtype)
        self.__sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')


    def writemail(self):
        self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
        self.__sslclientSocket.send(b'Content-Type: text/html;charset=utf-8\r\n')
        self.__sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
        self.mailcontent=input("请输入邮件正文：\n")
        time.sleep(1)
        self.__sslclientSocket.sendall(b'%s\r\n'%self.mailcontent.encode('utf-8'))

    def addfile(self):
        filepath=input("请输入文件路径：")
        time.sleep(1)
        # filepath=filepath.replace('\\','/')
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            #print(filename)
            time.sleep(0.1)
            self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
            self.__sslclientSocket.send(self.msgfileType)
            self.msgfilename = b"Content-Disposition: attachment; filename='%s'\r\n" % filename.encode('utf-8')
            self.__sslclientSocket.send(self.msgfilename)
            #print(self.msgfilename)
            self.__sslclientSocket.send(b'Content-Transfer-Encoding:base64\r\n\r\n')
            self.__sslclientSocket.send(self.msg)
            #print(1)
            time.sleep(0.1)
            fb = open(filepath,'rb')
            while True:
                filedata = fb.read(1024)
                # print(filedata)
                if not filedata:
                    break
                self.__sslclientSocket.send(base64.b64encode(filedata))
                time.sleep(1)
            fb.close()
            #print(2)
            time.sleep(0.1)


    def addimg(self):
        self.mailcontent = input("请输入邮件正文：")
        time.sleep(1)
        filepath = input("请输入图片路径：")
        time.sleep(1)
        # filepath = filepath.replace('\\', '/')
        if os.path.isfile(filepath):
            # print(1)
            time.sleep(0.1)
            filename = os.path.basename(filepath)
            randomid = filename.split('.')[1]+str(random.randint(1000, 9999))
            # print(randomid)
            time.sleep(0.1)
            self.msgimgId = b'Content-ID:%s\r\n' % randomid.encode('utf-8')
            self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
            self.__sslclientSocket.send(self.msgimgtype)
            self.__sslclientSocket.send(self.msgimgId)
            self.msgimgname = b"Content-Disposition: attachment; filename='%s'\r\n" % filename.encode('utf-8')
            self.__sslclientSocket.send(self.msgfilename)
            # print(self.msgimgId)
            time.sleep(0.1)
            self.__sslclientSocket.send(b'Content-Transfer-Encoding:base64\r\n\r\n')
            self.__sslclientSocket.send(self.msg)
            fb = open(filepath, 'rb')
            while True:
                filedata = fb.read(1024)
                # print(filedata)
                if not filedata:
                    break
                self.__sslclientSocket.send(base64.b64encode(filedata))
                time.sleep(0.1)
            fb.close()
            # print(1)
            time.sleep(0.1)
            self.__sslclientSocket.send(b'\r\n\r\n' + self.msgboundary)
            self.__sslclientSocket.send(self.msgtexthtmltype)
            self.__sslclientSocket.send(b'Content-Transfer-Encoding:8bit\r\n\r\n')
            msgimgscr = b'<img src="cid:%s">'%randomid.encode('utf-8')
            # print(1)
            time.sleep(0.1)
            self.__sslclientSocket.send(msgimgscr)
            # print(msgimgscr)
            time.sleep(0.1)
            self.__sslclientSocket.sendall(b'%s' % self.mailcontent.encode('utf-8'))
            # print(msgimgscr)
            time.sleep(0.1)

    def sendmail(self):
        # self.addimg()
        # print(1)
        # time.sleep(1)
        # self.addfile()
        # print(2)
        # self.__sslclientSocket.send(self.endmsg)
        bool_addimg = input("是否添加图片<Y/N>:")
        bool_addfile = input("是否添加附件<Y/N>:")
        if bool_addimg.lower() == 'y':
            if bool_addfile.lower() == 'y':
                self.addimg()
                print(1)
                self.addfile()
                print(2)
                self.__sslclientSocket.send(self.endmsg)
            else:
                self.addimg()
                self.__sslclientSocket.send(self.endmsg)
        else:
            if bool_addfile.lower() == 'y':
                self.writemail()
                self.addfile()
                self.__sslclientSocket.send(self.endmsg)
            else:
                self.writemail()
                self.__sslclientSocket.send(self.endmsg)



    def quitconnect(self):
        self.__sslclientSocket.send(self.quitCommand)


if __name__ == '__main__':
    try:
        sendmail = SendMail()
        sendmail.socketconnet()
        sendmail.login()
        sendmail.sender()
        sendmail.recipient()
        sendmail.senddata()
        sendmail.sendsubject()
        sendmail.sendmail()
        time.sleep(1)
        print("发送成功！")
        sendmail.quitconnect()
    except Exception:
            print(Exception)
    finally:
        exit(0)
