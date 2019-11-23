from mylib.smtp_socket import SMTPSocket
import uuid
from email.mime.text import MIMEText
from email.header import Header
from mylib.coder import encode_header
from mylib.code_logging import Logger
import dkim

_domain = 'bmw1984.com'
_receivers = '914081010@qq.com'
logging = Logger('send_email.log').get_log()
_sender = f'service@{_domain}'
content = open('templates/type_1.html', encoding='utf-8')
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
service.debuglevel = 1
# service.ehlo()
dkim_selector = b's1'
dkim_domain = b'bmw1984.com'
with open('conf/rsaky.pem') as fh:
    DKIM_PRIVATE_KEY = fh.read()
    # lines = re.split(b"\r?\n", bytes(DKIM_PRIVATE_KEY, encoding='utf-8'))
    # print(lines)
    signature = dkim.sign(
        message=message.as_bytes(),
        selector=dkim_selector,
        domain=dkim_domain,
        privkey=bytes(DKIM_PRIVATE_KEY, encoding='utf-8'),
    )
    message['DKIM-Signature'] = bytes.decode(signature.lstrip(b"DKIM-Signature: "))
    # print(message.as_string())
    try:
        data = service.send_mail(_sender, _receivers, message.as_string())
    except Exception:
        print('发送失败')
    logging.info(f'{_receivers} 邮件发送成功！ {data}')
