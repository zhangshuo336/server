from django.conf.urls import url
import views

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^list/(\d+)/(\d+)/$',views.listPage,name='listPage'),
    url(r'^details/(\d+)/$',views.details,name='details'),
    url(r'^registers/$',views.registers,name='registers'),
    url(r'^logins/$',views.logins,name='logins'),
    url(r'^verify/$',views.verify,name='verify'),
    url(r'^verifyTest/$',views.verifyTest,name='verifyTest'),
    url(r'^sendCode/$',views.sendCode,name='sendCode'),
    url(r'^checkMailCode/$',views.checkMailCode,name='checkMailCode'),
    url(r'^userRegister/$',views.userRegister,name='userRegister'),
    url(r'^checkUname/$',views.checkUname,name='checkUname'),
    url(r'^checkPassword/$',views.checkPassword,name='checkPassword'),
    url(r'^backUp/$',views.backUp,name='backUp'),
    url(r'^loginVerify/$', views.loginVerify, name='loginVerify'),
    url(r'^loginVerifyTest/$', views.loginVerifyTest, name='loginVerifyTest'),
    url(r'^user_center/$',views.user_center,name="user_center"),
    url(r'^pwd_reset_send_code/$',views.pwd_reset_send_code,name='pwd_reset_send_code'),
    url(r'^pwd_reset_checkmailcode',views.pwd_reset_checkmailcode,name='pwd_reset_checkmailcode'),



]