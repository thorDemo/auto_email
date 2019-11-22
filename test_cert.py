import smtplib
from email.mime.text import MIMEText
from email.header import Header


zhengwen = '这个月的财务报表有问题，来的时候带上资料'
fajianr = 'hdejbv@163.com'
shoujianr = '914081010@qq.com'
zhuti = '明天来我办公室一趟'
messeng=MIMEText(zhengwen, 'plain', 'utf-8')
messeng['From'] = Header(fajianr,'utf-8')
messeng['TO'] = Header(shoujianr,'utf-8')
subject = zhuti
messeng['Subject'] = Header(subject, 'utf-8')


def yxwz():
    try:
        smtp=smtplib.SMTP()
        smtp.connect('smtp.163.com', '25')
        smtp.login('hdejbv@163.com', 'a11195')
        smtp.sendmail('hdejbv@163.com', ['914081010@qq.com'], messeng.as_string())
        smtp.quit()
        print('[*]邮件发送成功')
    except Exception as e:
      print('[-]发送失败,报错原因:', e)

yxwz()
