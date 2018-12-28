#coding=utf-8
from celery import task
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import random



# 发送邮箱验证码工具函数
def mailCode(addr):
    emailAddr = addr
    my_sender = 'qiyuemail@126.com'  # 发件人邮箱账号
    my_pass = '41512710zsa'  # 发件人邮箱密码
    my_user = emailAddr  # 收件人邮箱账号，我这边发送给自己
    randCode = random.randint(100000,999999)
    try:
        content = '<div style="background-color:#69F1F2;width:100%;height:300px;text-align:center;line-height:300px;"><b style="color:#EA2C52;font-size:40px;font-weight:blod;">'+str(randCode)+'</b></div>'
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = formataddr(["七月网", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "邮箱验证码"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.126.com",465)  # 发件人邮箱中的SMTP服务器，端口是25加密端口465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        return randCode
    except Exception as e:
        return False


# 发送邮箱验证码逻辑调用工具函数发送验证码由于存在发送失败的情况利用循环保证发送成功
def asyncSendCode(request):
    addr = request.GET['mailAddr']
    for i in range(10):
        test = mailCode(addr)
        if test:
            request.session['mailCode'] = test
            request.session['timeOut'] =time.time()
            return
        else:
            # 最多尝试4次若都失败将通知前端
            if i<9:
                time.sleep(0.8)
            else:
                return