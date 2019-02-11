#coding=utf-8
import os
from django.shortcuts import render
from myblog import settings
from models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from hashlib import sha1

def recvUserMsgs(request):
    nick_error = 0
    gender_error = 0
    age_error = 0
    error = {}
    userid = request.session.get('userid','')
    data = request.FILES.get('userpic',None)
    picName = os.path.join(settings.MEDIA_ROOT,str(userid)+data.name)
    with open(picName,'wb')as f:
        for p in data:
            f.write(p)
    nickName = request.POST.get('nickname','')
    gender = request.POST.get('sex',1)
    age = request.POST.get('age','')
    if nickName:
        l = len(nickName)
        if (l>1) and (l<20):
            nick_error = 0
        else:
            error['nick_error'] = u'昵称长度不符合要求'
    else:
        error['nick_error'] = u'昵称不能为空字符串'
    agetest = str(age)
    if agetest.isdigit():
        if (age>0) and (age<121):
            age_error = 0
        else:
            error['age_error'] = u'输入正常年龄!'
    else:
        error['age_error']= u'输入正确格式的年龄!'
    if (gender ==0) or (gender == 1):
        gender_error = 0
    else:
        error['age_error']='传送布尔型数据'
    if (gender_error == 0) and (age_error == 0) and (nick_error == 0):
        user = User.objects.get(id=userid)
        user.loveName = nickName
        user.gender = gender
        user.age = age
        user.userPic = '/statics/media/'+str(userid)+data.name
        user.save()
        content = {'pageTitle':'信息修改反馈','nick_error':'格式正确!','gender_error':'格式正确!','age_error':'格式正确!'}
        return render(request,'user_result.html',content)
    else:
        return render(request,'user_result.html',error)


def pwd_reset(request):
    return render(request,'pwd_reset.html')

def recv_reset_pwd(request):
    userName = request.POST.get('user_name', '')
    password = request.POST.get('pwd', '')
    password2 = request.POST.get('cpwd', '')
    # 这里需要对用户穿进来的数据进行二次正则验证
    userName_error = False
    password_error = False
    l = len(userName)
    if (l > 4) and (l < 21):
        pass
    else:
        userName_error = True
    if password == password2:
        pl = len(password)
        if pl > 7 and pl < 21:
            pass
        else:
            password_error = True
    else:
        password_error = True
    if userName_error or password_error:
        return HttpResponse('建议您使用能够前端注册避免不必要的错误!')
    else:
        num = User.objects.filter(userName=userName).count()
        if num == 1:
            s1 = sha1()
            s1.update(password)
            sha1_password = s1.hexdigest()
            u = User.objects.get(userName=userName)
            u.password = sha1_password
            u.save()
            request.session.flush()
            return HttpResponseRedirect(reverse('htmlPageApp:logins'))
        else:
            return HttpResponse('建议您使用能够前端注册避免不必要的错误!')



