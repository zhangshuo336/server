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
    url(r'^pwd_reset_checkmailcode/$',views.pwd_reset_checkmailcode,name='pwd_reset_checkmailcode'),
    url(r'^yellow_page/$',views.yellow_page,name='yellow_page'),
    url(r'^num_phone_find/$',views.num_phone_find,name='num_phone_find'),
    url(r'^ip_find/$',views.ip_find,name='ip_find'),
    url(r'^shici_search/$',views.shici_search,name='shici_search'),
    url(r'shici_search_title',views.shici_search_title,name='shici_search_title'),
    url(r'shici_search_authors',views.shici_search_authors,name='shici_search_authors'),
    url(r'about_me',views.about_me,name='about_me'),
    url(r'^qq_login_page/$',views.qq_login_page,name='qq_login_page'),
    url(r'^qq_login/$',views.qq_login,name='qq_login'),



]