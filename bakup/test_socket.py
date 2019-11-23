import socket
import re
"""
=== Trying mx3.qq.com:25...
=== Connected to mx3.qq.com.
<-  220 newxmmxszc27.qq.com MX QQ Mail Server.
 -> n1127-3.com.com
<-  250-newxmmxszc27.qq.com
<-  250-STARTTLS
<-  250-SIZE 73400320
<-  250 OK
 -> MAIL FROM:<root@xin1127-3.com.com>
<-  250 OK.
 -> RCPT TO:<914081010@qq.com>
<-  250 OK 1
 -> DATA
<-  354 End data with <CR><LF>.<CR><LF>.
 -> Date: Sat, 23 Nov 2019 13:33:46 +0800
 -> To: 914081010@qq.com
 -> From: root@xin1127-3.com.com
 -> Subject: test Sat, 23 Nov 2019 13:33:46 +0800
 -> X-Mailer: swaks v20130209.0 jetmore.org/john/code/swaks/
 -> 
 -> This is a test mailing
 -> 
 -> .

"""
# connection
service_ip = 'mx3.qq.com'
print(f'connect {service_ip}')
true_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
true_socket.connect((service_ip, 25))
res = true_socket.recv(4096)
print(res, 1)
data = str(res, encoding='utf-8').split(' ')

request = f"HELO bmw1984.com\r\n"
print(f'>{request}')
true_socket.sendall(request.encode("utf-8"))
res = true_socket.recv(4096)
print(res, 2)

# request = f"EHLO bmw1984.com\r\n"
# print(f'>{request}')
# true_socket.sendall(request.encode("utf-8"))
# res = true_socket.recv(4096)
# print(res, 3)

# from
request = "MAIl FROM:<admin@bmw1984.com>\r\n"
true_socket.sendall(request.encode("utf-8"))
res = true_socket.recv(4096)
print(res, 4)

# rcpt
request = "RCPT TO:<9204163032@qq.com>\r\n"
true_socket.sendall(request.encode("utf-8"))
res = true_socket.recv(4096)
print(res)

# data
request = "DATA\r\n"
true_socket.sendall(request.encode("utf-8"))
res = true_socket.recv(4096)
print(res)

# send
request = '''
...sends body of mail message...
...Dear xxx...
\r\n
'''
true_socket.sendall(request.encode("utf-8"))
res = true_socket.recv(4096)
print(res)

# close
true_socket.close()
