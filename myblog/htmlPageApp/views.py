#coding=utf-8
from django.shortcuts import render,render_to_response
from artDataApp.models import ArtData
from django.core.paginator import Paginator
from createCode.myCreate import picChecker
import uuid
import cStringIO
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from blogUserApp.models import User
from hashlib import sha1
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import random
from tonApp.models import Ton
from django.template import RequestContext
import re
import json, urllib,urllib2
from urllib import urlencode
from models import visitLog
from django.core.urlresolvers import reverse
from django.conf import settings
import requests
from django.views.decorators.cache import cache_page
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
# import json, urllib
# from urllib import urlencode
#
# url = "http://apis.juhe.cn/ip/ip2addr"
# params = {
#     "ip": "112.51.53.11",  # 需要查询的IP地址或域名
#     "key": "您申请的ApiKey",  # 应用APPKEY(应用详细页查询)
# }
# params = urlencode(params)
# f = urllib.urlopen(url, params)
# content = f.read()
# res = json.loads(content)
# if res:
#     print(res)
# else:
#     print("请求异常")
def index(request):
    url = "http://apis.juhe.cn/ip/ip2addr"
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    params = {
        "ip": ip,  # 需要查询的IP地址或域名
        "key": "47285fd589de069f554c2717c98bda50",  # 应用APPKEY(应用详细页查询)
        }
    params = urlencode(params)
    f = urllib.urlopen(url, params)
    content = f.read()
    res = json.loads(content)
    res=res['result']
    if res:
        u = visitLog()
        u.ip = ip
        u.area = res['area']
        u.compy = res['location']
        u.save()
    else:
        pass
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
    num = data.lookTip
    num+=1
    data.lookTip = num
    data.save()
    tonlist = Ton.objects.filter(tip_id=int(idnum))
    url = request.get_full_path()
    content = {'data':data,'tonlist':tonlist}
    resp = render_to_response('detail.html',content,context_instance=RequestContext(request))
    resp.set_cookie('detailurl',url)
    return resp

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

def pwd_reset_send_code(request):
    uname = request.GET.get('uname',uuid.uuid4())
    data = User.objects.filter(userName=uname).count()
    if data == 1:
        addr = User.objects.get(userName=uname).email
        for i in range(10):
            test = mailCode(addr)
            if test:
                request.session['pwd_reset_mailcode'] = test
                request.session['pwd_reset_timeOut'] = time.time()
                return HttpResponse(1)
            else:
                # 最多尝试10次若都失败将通知前端
                if i < 9:
                    time.sleep(0.2)
                else:
                    return HttpResponse(0)
    else:
        return JsonResponse('建议采用前端修改密码保证正顺利进行')

def pwd_reset_checkmailcode(request):
    userCode = request.GET['mailCode']
    timeOut = time.time() - request.session.get('pwd_reset_timeOut', 0)
    # 这里定义验证码的有效期最多位10分钟
    if timeOut > 600:
        del request.session['pwd_reset_mailcode']
        return HttpResponse(0)
    mailCode = request.session['pwd_reset_mailcode']
    if userCode == str(mailCode):
        return HttpResponse(1)
    else:
        return HttpResponse(0)

# 采用异步方式发送邮箱验证码缩短用户等待时间
def sendCode(request):
    addr = request.GET['mailAddr']
    for i in range(10):
        test = mailCode(addr)
        if test:
            request.session['mailCode'] = test
            request.session['timeOut'] = time.time()
            return HttpResponse(1)
        else:
            # 最多尝试4次若都失败将通知前端
            if i < 9:
                time.sleep(0.6)
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
    userName = request.POST.get('user_name','')
    password = request.POST.get('pwd','')
    password2 = request.POST.get('cpwd','')
    userEmail = request.POST.get('email','')
    # 这里需要对用户穿进来的数据进行二次正则验证
    userName_error = False
    password_error = False
    userEmail_error = False
    l = len(userName)
    if (l>4) and (l<21):
        pass
    else:
        userName_error = True
    if password == password2:
        pl = len(password)
        if pl>7 and pl<21:
            pass
        else:
            password_error = True
    else:
        password_error = True
    if re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',userEmail):
        pass
    else:
        userEmail_error = True
    if userName_error or password_error or userEmail_error:
        return HttpResponse('建议您使用能够前端注册避免不必要的错误!')
    else:
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
        l = User.objects.get(userName=userName)
        request.session['userid'] = l.id
        request.session['uname'] = userName
        del request.session['mailCode']
        del request.session['verify']
        del request.session['timeOut']
        return HttpResponseRedirect(reverse('htmlPageApp:index'))


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
@loginTest
def user_center(request):
    id = request.session.get('userid')
    user = User.objects.get(id=id)
    content = {'user':user,'pageTitle':'七月-用户中心'}
    return render(request,"user_center.html",content)

def yellow_page(request):
    # url = "http://apis.juhe.cn/ip/ip2addr"
    # params = {
    #     "ip": "112.51.53.11",  # 需要查询的IP地址或域名
    #     "key": "您申请的ApiKey",  # 应用APPKEY(应用详细页查询)
    # }
    # params = urlencode(params)
    # f = urllib.urlopen(url, params)
    # content = f.read()
    # res = json.loads(content)
    # if res:
    #     print(res)
    # else:
    #     print("请求异常")

    # 热点新闻
    url = 'https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_society_suda&top_time=today&top_show_num=30&top_order=DESC'
    f = urllib.urlopen(url)
    content = f.read()
    res = content[11:-2]
    res =  json.loads(res)
    if res:
        top = res['data']
    else:
        top = []

        # 国际新闻
    url = 'https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=gjxwpl&top_time=today&top_show_num=60&top_order=DESC'
    f = urllib.urlopen(url)
    content = f.read()
    res = content[11:-2]
    res = json.loads(res)
    if res:
        guoji = res['data']
    else:
        guoji = []
        # 国内新闻
    url = 'https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_china_suda&top_time=today&top_show_num=60&top_order=DESC'
    f = urllib.urlopen(url)
    content = f.read()
    res = content[11:-2]
    res = json.loads(res)
    if res:
        guonei = res['data']
    else:
        guonei = []
        # 军事新闻
    url = 'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_mil_suda&top_time=today&top_show_num=30&top_order=DESC'
    f = urllib.urlopen(url)
    content = f.read()
    res = content[11:-2]
    res = json.loads(res)
    if res:
        junshi = res['data']
    else:
        junshi = []
        # 社会新闻
    url = 'https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_society_suda&top_time=today&top_show_num=60&top_order=DESC'
    f = urllib.urlopen(url)
    content = f.read()
    res = content[11:-2]
    res = json.loads(res)
    if res:
        shehui = res['data']
    else:
        shehui = []
    content = {
        'top':top,
        'shehui':shehui,
        'junshi':junshi,
        'guonei':guonei,
        'guoji':guoji,
        'pageTitle':'七月-生活服务'
    }
    return render(request,'yellow_page.html',content)

def num_phone_find(request):
    num = request.GET.get('num','')
    if str(num).isdigit():
        if len(num) == 11:
            url = 'http://apis.juhe.cn/mobile/get'
            params = {
                'key':'0ceb712c883e9bfe5e0e813f005523bd',
                'phone':num
            }
            params = urlencode(params)
            f = urllib.urlopen(url,params)
            content = f.read()
            resp = json.loads(content)
            resp = resp['result']
            if resp:
                data = resp
            else:
                data = {}
            return JsonResponse(data)
        else:
            return JsonResponse({})
    else:
        return JsonResponse({})

def ip_find(request):
    ip = request.GET.get('num','')
    if re.match(r'(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})(\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})){3}$',ip):
        url = "http://apis.juhe.cn/ip/ip2addr"
        params = {
            "ip": ip,  # 需要查询的IP地址或域名
            "key": "47285fd589de069f554c2717c98bda50",  # 应用APPKEY(应用详细页查询)
        }
        params = urlencode(params)
        f = urllib.urlopen(url, params)
        content = f.read()
        res = json.loads(content)
        res = res['result']
        if res:
            return JsonResponse(res)
        else:
            return JsonResponse({})
    else:
        return JsonResponse({})

def shici_search(request):
    msg = request.GET.get('msg','').encode('utf-8')
    url = 'https://api.apiopen.top/likePoetry?name='+msg
    # params = {
    #     'name':msg
    # }
    # # params = urlencode(params)
    f = urllib.urlopen(url)
    content = f.read().decode('utf-8')
    resp = json.loads(content)
    resp = resp['result']
    return JsonResponse(resp,safe=False)

def shici_search_title(request):
    msg = request.GET.get('msg', '').encode('utf-8')
    url = 'https://api.apiopen.top/searchPoetry?name=' + msg
    # params = {
    #     'name':msg
    # }
    # # params = urlencode(params)
    f = urllib.urlopen(url)
    content = f.read().decode('utf-8')
    resp = json.loads(content)
    resp = resp['result']
    return JsonResponse(resp, safe=False)

def shici_search_authors(request):
    msg = request.GET.get('msg', '').encode('utf-8')
    url = 'https://api.apiopen.top/searchAuthors?name=' + msg
    # params = {
    #     'name':msg
    # }
    # # params = urlencode(params)
    f = urllib.urlopen(url)
    content = f.read().decode('utf-8')
    resp = json.loads(content)
    resp = resp['result']
    resp = resp[0]
    name = resp['name']
    desc = resp['desc'].split()[0]
    resp = {
        'name':name,
        'desc':desc
    }
    resp = [resp]
    return JsonResponse(resp, safe=False)

def about_me(request):
    return render(request,'about_me.html',{'pageTitle':'关于我'})

# 返回QQ登陆界面
def qq_login_page(request):
    state = random.randint(100000,999999)
    request.session['state'] = state
    client_id = '101544383'
    callback = 'http%3a%2f%2f127.0.0.1%3a8000%2fqq_login'
    login_url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=%s&redirect_uri=%s&state=%s'%(client_id, callback, state)
    # login_url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=101544383&redirect_uri=http%3a%2f%2f127.0.0.1%3a8000%2fqq_login&state = 236597'
    # url = 'https://graph.qq.com/oauth2.0/authorize'
    # params = {
    #     'response_type':'code',
    #     'client_id':client_id,
    #     'redirect_uri':callback,
    #     'state':state
    # }
    # login_url = urllib.urlencode()
    return HttpResponseRedirect(login_url)

def parse_jsonp(jsonp_str):
    try:
        return re.search(r'^[^(]*?\((.*)\)[^)]*$', jsonp_str).group(1)
    except:
        raise ValueError('无效数据！')
# 获取QQ用户信息
def qq_login(request):
    if int(request.session['state']) == int(request.GET['state']):
        code = request.GET['code']
        client_id = '101544383'
        client_secret = 'b8faa3df6d90f0d3d9e8b3450af9d256'
        callback = 'http%3a%2f%2f127.0.0.1%3a8000%2fqq_login'
        login_url = 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s'% (code, client_id, client_secret, callback)
        response = urllib2.urlopen(login_url).read().decode()
        access_token = re.split('&', response)[0]
        res = urllib2.urlopen('https://graph.qq.com/oauth2.0/me?' + access_token).read()
        openid = json.loads(parse_jsonp(res))['openid']
        userinfo = urllib2.urlopen('https://graph.qq.com/user/get_user_info?oauth_consumer_key=%s&openid=%s&%s' % (client_id, openid, access_token)).read()
        userinfo = json.loads(userinfo)
        if User.objects.filter(userName=openid).count():
            request.session['uname'] = User.objects.get(userName=openid).loveName
            request.session['userid'] = User.objects.get(userName=openid).id
            return HttpResponseRedirect(reverse('htmlPageApp:index'))
        else:
            u = User()
            u.userName = openid
            mysha1 = sha1()
            mysha1.update('000000')
            passwd = mysha1.hexdigest()
            u.password = passwd
            u.loveName = userinfo['nickname']
            if userinfo['gender'] == '女':
                u.gender = False
            else:
                u.gender = True
            u.age = int(userinfo['year'])
            u.userPic = userinfo['figureurl_qq_1']
            u.email = 'a'
            u.save()
            request.session['uname'] = userinfo['nickname']
            request.session['userid'] = User.objects.get(userName=openid).id
            return HttpResponseRedirect(reverse('htmlPageApp:index'))
    else:
        return HttpResponse('error')

        # 微信第三方登陆代码
def wechat_page(request):
    pass
def sina_login_page(request):
    state = random.randint(100000, 999999)
    request.session['sina_state'] = state
    client_id = settings.SINA_APP_KEY
    callback = 'http://127.0.0.1:8000/sina_login'
    login_url = 'https://api.weibo.com/oauth2/authorize?client_id=%s&redirect_uri=%s&state=%s' % (client_id, callback, state)
    return HttpResponseRedirect(login_url)
def sina_login(request):
    if int(request.session['sina_state']) == int(request.GET['state']):
        code = request.GET['code']
        client_id = settings.SINA_APP_KEY
        client_secret = settings.SINA_APP_SECRET
        callback = 'http://127.0.0.1:8000/sina_login'
        url = 'https://api.weibo.com/oauth2/access_token'
        params={
            "client_id":client_id,
            "client_secret":client_secret,
            "code":code,
            "grant_type":"authorization_code",
            "redirect_uri":callback
        }
        # params = urllib.urlencode(params)
        # requ= urllib2.Request(url,data=params)
        # response = urllib2.urlopen(requ)
        response = requests.post(url,data=params)
        # print (response.json()['uid'])
        usermsg_info_url = 'https://api.weibo.com/2/users/show.json'
        data={
            'access_token':response.json()['access_token'],
            'uid':response.json()['uid']
        }
        response = requests.get(usermsg_info_url,params=data)
        # print (response)
        # return HttpResponse(response)
        if User.objects.filter(userName=response.json()['idstr']).count():
            request.session['uname'] = User.objects.get(userName=response.json()['idstr']).loveName
            request.session['userid'] = User.objects.get(userName=response.json()['idstr']).id
            return HttpResponseRedirect(reverse('htmlPageApp:index'))
        else:
            u = User()
            u.userName = response.json()['idstr']
            mysha1 = sha1()
            mysha1.update('000000')
            passwd = mysha1.hexdigest()
            u.password = passwd
            u.loveName = response.json()['name']
            if response.json()['gender'] == 'f':
                u.gender = False
            else:
                u.gender = True
            u.age = 1
            u.userPic = response.json()['profile_image_url']
            u.email = 'a'
            u.save()
            request.session['uname'] = response.json()['name']
            request.session['userid'] = User.objects.get(userName=response.json()['idstr']).id
            return HttpResponseRedirect(reverse('htmlPageApp:index'))
    else:
        return HttpResponse('ERROR')