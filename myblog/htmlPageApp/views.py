#coding=utf-8
from django.shortcuts import render
from artDataApp.models import ArtData
from django.core.paginator import Paginator
from createCode.myCreate import picChecker
import uuid
import cStringIO
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import random
from blogUserApp.models import User
from hashlib import sha1



# 装饰器用于对用户登陆状态的检测
def loginTest(func):
    def loginCheck(request,*args,**kwargs):
        if request.session.has_key('uname'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect(reverse('htmlPageApp:logins'))
            red.set_cookie('url',request.get_full_path())
            return red
    return loginCheck


# 返回前端首页并传递最新年的5条数据
def index(request):
    artDataList = ArtData.objects.order_by('-id')[0:5]
    content = {'artDataList':artDataList,'pageTitle':'七月-首页'}
    return render(request,'index.html',content)

# 返回各板块列表页并根据列表页的不同确定显示内容
def listPage(request,pagenum,sortnum):
        dataList = ArtData.objects.filter(artDivide=int(sortnum))
        paginator = Paginator(dataList,3)
        page = paginator.page(int(pagenum))
        # 当想增加新的板块时增加content并吧pageName修改了就行
        if sortnum == '0':
            content = {'pageName': '技术分享','page':page,'sortnum':0,'pageTitle':'七月-技术分享'}
        elif sortnum == '1':
            content = {'pageName': '读书笔记', 'page': page,'sortnum':1,'pageTitle':'七月-读书笔记'}
        else:
            content = {'pageName': '读书笔记', 'page': page,'sortnum':1,'pageTitle':'七月-读书笔记'}
        return render(request, 'list.html', content)



# 显示每条数据的详细信息
@loginTest
def details(request,idnum):
    data = ArtData.objects.get(pk=int(idnum))
    content = {'data':data}
    return render(request,'detail.html',content)

# 返回注册页
def registers(request):
    return render(request,'register.html')




# 返回登陆页
def logins(request):
    return render(request,'login.html')


# 生成验证码图片并传回前端
def verify(request):
    str,pic = picChecker().createChecker()
    request.session['verify'] = str
    buf = cStringIO.StringIO()
    pic.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')

# 对前端传回的验证码进行判断
def verifyTest(request):
    userCode = request.GET['piccatcode']
    sessionCode = request.session.get('verify',uuid.uuid4())
    if userCode.lower() == sessionCode.lower():
        return HttpResponse(1)
    else:
        return HttpResponse(0)

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

        server = smtplib.SMTP_SSL("smtp.126.com",465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        return randCode
    except Exception as e:
        return False

# 发送邮箱验证码逻辑调用工具函数发送验证码由于存在发送失败的情况利用循环保证发送成功
def sendCode(request):
    addr = request.GET['mailAddr']
    for i in range(5):
        test = mailCode(addr)
        if test:
            request.session['mailCode'] = test
            request.session['timeOut'] =time.time()
            return HttpResponse(1)
        else:
            # 最多尝试4次若都失败将通知前端
            if i<4:
                time.sleep(0.8)
            else:
                return HttpResponse(0)

# 核对前端提供的邮箱验证码的正确性
def checkMailCode(request):
    userCode = request.GET['mailCode']
    timeOut = time.time() - request.session.get('timeOut',0)
    # 这里定义验证码的有效期最多位10分钟
    if timeOut>600:
        del request.session['mailCode']
        return HttpResponse(0)
    mailCode = request.session['mailCode']
    if userCode == str(mailCode):
        return HttpResponse(1)
    else:
        return HttpResponse(0)


# 用户注册逻辑
def userRegister(request):
    userName = request.POST['user_name']
    password = request.POST['pwd']
    userEmail = request.POST['email']
    # 这里需要对用户穿进来的数据进行二次正则验证
    s1 = sha1()
    s1.update(password)
    sha1_password = s1.hexdigest()
    u = User()
    u.userName = userName
    u.loveName = userName
    u.password = sha1_password
    u.email = userEmail
    u.userPic = 'a'
    u.save()
    del request.session['mailCode']
    del request.session['verify']
    del request.session['timeOut']
    return HttpResponseRedirect(reverse('htmlPageApp:logins'))


# 核对用户名是否存在
def checkUname(request):
    uname = request.GET['uname']
    data = User.objects.filter(userName=uname).count()
    return JsonResponse({'data':data})


# 执行登陆逻辑判断验证账号密码的存在以及正确性判断用户是否让浏览器记住用户名
def checkPassword(request):
    uname = request.POST['username']
    passwd = request.POST['pwd']
    flag = request.POST.get('flag',0)
    if User.objects.filter(userName=uname).count():
        passwd1 = User.objects.get(userName=uname).password
        mysha1 = sha1()
        mysha1.update(passwd)
        passwd2 = mysha1.hexdigest()
        if passwd1 == passwd2:
            if flag:
                userurl = request.COOKIES.get('url','/')
                red = HttpResponseRedirect(userurl)
                request.session['uname'] = uname
                request.session['userid'] = User.objects.get(userName=uname).id
                red.set_cookie('uname',uname)
                red.delete_cookie('url')
                del request.session['loginVerify']
                return red
            else:
                userurl = request.COOKIES.get('url', '')
                red = HttpResponseRedirect(userurl)
                red.set_cookie('uname', '',max_age=-1)
                request.session['uname'] = uname
                request.session['userid'] = User.objects.get(userName=uname).id
                red.delete_cookie('url')
                del request.session['loginVerify']
                return red
        else:
            content = {'uname':uname,'passwd':passwd,'pwderror':1,'unameerror':0}
            return render(request,'login.html',content)
    else:
        content = {'uname':uname,'passwd':passwd,'pwderror':0,'unameerror':1}
        return render(request, 'login.html', content)

# 用户注销登陆
def backUp(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('htmlPageApp:index'))

# 生成登陆时的验证码图片并传回前端
def loginVerify(request):
    str, pic = picChecker().createChecker()
    request.session['loginVerify'] = str
    buf = cStringIO.StringIO()
    pic.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')

# 登陆验证码的判断视图
def loginVerifyTest(request):
    userCode = request.GET['user_code']
    sessionCode = request.session['loginVerify']
    if userCode.lower() == sessionCode.lower():
        return HttpResponse(1)
    else:
        return HttpResponse(0)
