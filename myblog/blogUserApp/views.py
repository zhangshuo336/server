#coding=utf-8
from django.shortcuts import render
import os
from myblog import settings
# Create your views here.
from models import User

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


def hah(request):
    return render(request,'user_result.html')


