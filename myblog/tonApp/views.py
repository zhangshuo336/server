#coding=utf-8
from django.shortcuts import render
from models import Ton
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from htmlPageApp.views import loginTest
from artDataApp.models import ArtData

# Create your views here.
@loginTest
def recvTon(request):
    # 用户id
    # 文章id
    # 评论内容
    # 点赞数默认为0
    userurl = request.COOKIES.get('detailurl','/')
    ton = Ton()
    ton.tonMesage_id = request.session.get("userid",'')
    a= request.POST.get('arttip')
    data = ArtData.objects.get(pk=int(a))
    num = data.sayTip
    num+=1
    data.sayTip = num
    data.save()
    ton.tip_id = int(a)
    ton.tonArea = request.POST.get('userTon','')
    ton.tonGoodTip = 0
    ton.save()
    print userurl
    return HttpResponseRedirect(userurl)
