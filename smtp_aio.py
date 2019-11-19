import asyncio
import uuid
from email.mime.text import MIMEText
from email.header import Header
from mylib.coder import encode_header
from mylib.code_logging import Logger
import smtplib

from smtplibaio import SMTP, SMTP_SSL

logging = Logger('send_email.log').get_log()


async def send_email():
    sender = "serivces@jnyhldw.com"
    receivers = "914081010@qq.com"

    content = open('templates/type_1.html', encoding='utf-8')
    message = MIMEText(content.read(), _subtype='html', _charset='utf-8')
    message['Accept-Language'] = "zh-CN"
    message['Accept-Charset'] = "ISO-8859-1,UTF-8"
    message['From'] = encode_header('宝马会娱乐城', sender)
    message['To'] = encode_header('超级VIP客户', receivers)
    message['Subject'] = Header('宝马会礼金大放送', 'utf-8')
    message['Received'] = 'from msc-channel180022225.sh(100.68.112.227) by smtp.aliyun-inc.com(127.0.0.1);'
    message['Message-ID'] = uuid.uuid4().__str__()
    message['MIME-Version'] = '1.0'
    message['Return-Path'] = 'smtp.jnyhldw.com'

    async with SMTP_SSL() as client:
        try:
            await client.sendmail(sender, receivers, message)
        except ConnectionRefusedError:
            logging.warning(f'{receivers} 无法连接本地服务器。')
        except smtplib.SMTPServerDisconnected:
            logging.warning(f'{receivers} 服务器意外断开连接。')
        except smtplib.SMTPSenderRefused:
            logging.warning(f'{receivers} 发件人地址被拒绝。')
        except smtplib.SMTPRecipientsRefused:
            logging.warning(f'{receivers} 所有收件人地址均被拒绝。')
        except smtplib.SMTPDataError:
            logging.warning(f'{receivers} SMTP服务器拒绝接受邮件数据。')
        except smtplib.SMTPConnectError:
            logging.warning(f'{receivers} 与服务器建立连接期间发生错误。')
        except smtplib.SMTPHeloError:
            logging.warning(f'{receivers} 服务器拒绝了我们的HELO消息。')
        except smtplib.SMTPNotSupportedError:
            logging.warning(f'{receivers} 服务器不支持尝试的命令或选项。')
        except smtplib.SMTPAuthenticationError:
            logging.warning(f'{receivers} 服务器不支持尝试的命令或选项。')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email())
    loop.close()
