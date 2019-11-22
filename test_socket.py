import socket
import re

host = "2000019.ip138.com"
port = 80
ip = socket.gethostbyname(host)
address = (ip, port)
try:
    local_ip = '46.151.157.115'
    print(f'设置本地IP：{local_ip}')
    true_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    true_socket.bind((local_ip, 50893))
    # s = socket.socket()
    s = true_socket
    s.connect(address)
    request = "GET / HTTP/1.1\r\n" \
              "Host: 2000019.ip138.com\r\n" \
              "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
              "Chrome/44.0.2403.125 Safari/537.36\r\n" \
              "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\r\n\r\n"
    s.sendall(request.encode("utf-8"))
    res = s.recv(4096)
    # print(res)
    if res:
        data = str(res, encoding='utf-8')
        data = data.split('\r\n')
        for line in data:
            if 'title' in line:
                print(line)
    else:
        print("visit {0} error".format(host))
except Exception as e:
    raise e
