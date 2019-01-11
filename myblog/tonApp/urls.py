# coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^recvton/$',views.recvTon,name="recvton"),
    url(r'^Good/$',views.goods,name="Good"),
    url(r'^tonGoodTip/$',views.tongoodtip,name="tonGoodTip"),
]