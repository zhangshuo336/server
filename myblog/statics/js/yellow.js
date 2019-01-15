$(function(){
//    $('.news_tag_top').css({'backgroundColor':'transparent','color':'red'})
    $('.news_tag_top').click(function(){$('.news_tag_top').css({'backgroundColor':'transparent','color':'red'}).siblings().css({'backgroundColor':'red','color':'#FFF'});
    $('.top').show();
    $('.top').siblings().hide();
    });

    $('.news_tag_shehui').click(function(){$('.news_tag_shehui').css({'backgroundColor':'transparent','color':'red'}).siblings().css({'backgroundColor':'red','color':'#FFF'});
    $('.shehui').show();
    $('.shehui').siblings().hide();
    });

    $('.news_tag_guonei').click(function(){$('.news_tag_guonei').css({'backgroundColor':'transparent','color':'red'}).siblings().css({'backgroundColor':'red','color':'#FFF'});
    $('.guonei').show();
    $('.guonei').siblings().hide();
    });

    $('.news_tag_guoji').click(function(){$('.news_tag_guoji').css({'backgroundColor':'transparent','color':'red'}).siblings().css({'backgroundColor':'red','color':'#FFF'});
    $('.guoji').show();
    $('.guoji').siblings().hide();
    });

    $('.news_tag_junshi').click(function(){$('.news_tag_junshi').css({'backgroundColor':'transparent','color':'red'}).siblings().css({'backgroundColor':'red','color':'#FFF'});
    $('.junshi').show();
    $('.junshi').siblings().hide();
    });
//功能导航栏
    $('.yel_tag_news').click(function(){$('.yel_tag_news').css({'backgroundColor':'transparent','color':'black'}).siblings().css({'color':'#FFF','backgroundColor':'#1E55E0'});
    $('.news').show();
    $('.news').siblings().hide();
    });

    $('.yel_tag_num_phone').click(function(){$('.yel_tag_num_phone').css({'backgroundColor':'transparent','color':'black'}).siblings().css({'color':'#FFF','backgroundColor':'#1E55E0'});
    $('.num_phone').show();
    $('.num_phone').siblings().hide();
    });

    $('.yel_tag_ip').click(function(){$('.yel_tag_ip').css({'backgroundColor':'transparent','color':'black'}).siblings().css({'color':'#FFF','backgroundColor':'#1E55E0'});
    $('.ip').show();
    $('.ip').siblings().hide();
    });

    $('.yel_tag_sfcard').click(function(){$('.yel_tag_sfcard').css({'backgroundColor':'transparent','color':'black'}).siblings().css({'color':'#FFF','backgroundColor':'#1E55E0'});
    $('.sfcard').show();
    $('.sfcard').siblings().hide();
    });

    $('.yel_tag_caipiao').click(function(){$('.yel_tag_caipiao').css({'backgroundColor':'transparent','color':'black'}).siblings().css({'color':'#FFF','backgroundColor':'#1E55E0'});
    $('.caipiao').show();
    $('.caipiao').siblings().hide();
    });

    $('.yel_tag_hcaipiao').click(function(){$('.yel_tag_hcaipiao').css({'backgroundColor':'transparent','color':'black'}).siblings().css({'color':'#FFF','backgroundColor':'#1E55E0'});
    $('.hcaipiao').show();
    $('.hcaipiao').siblings().hide();
    });
})