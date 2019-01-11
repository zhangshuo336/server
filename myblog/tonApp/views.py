#coding=utf-8
from django.shortcuts import render
from models import Ton,User_ton
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from htmlPageApp.views import loginTest
from artDataApp.models import ArtData
from blogUserApp.models import UserGood
from django.http import HttpResponse

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
    return HttpResponseRedirect(userurl)

@loginTest
def goods(request):
    ids = request.GET.get('tipid','')
    userid = request.session.get("userid",'')
    datalist = UserGood.objects.filter(art_id=int(ids)).all()
    for data in datalist:
        if int(data.user_id) == int(userid):
            return HttpResponse(0)
    newmsg = UserGood()
    newmsg.user_id = int(userid)
    newmsg.art_id = int(ids)
    newmsg.save()
    g = ArtData.objects.get(id=int(ids))
    num = g.goodTip
    num+=1
    g.goodTip = num
    g.save()
    return HttpResponse(1)

@loginTest
def tongoodtip(request):
    ids =request.GET.get('tonid','')
    userid = request.session.get('userid','')
    datalist = User_ton.objects.filter(ton_id=int(ids)).all()
    for data in datalist:
        if int(data.user_id) == int(userid):
            return HttpResponse(0)
    newmsg = User_ton()
    newmsg.user_id = int(userid)
    newmsg.ton_id = int(ids)
    newmsg.save()
    t = Ton.objects.get(id=int(ids))
    num = t.tonGoodTip
    num+=1
    t.tonGoodTip = num
    t.save()
    return HttpResponse(int(ids))

