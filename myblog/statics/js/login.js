//function check_uname(){
//    var username = $('.name_input').val();
//    if(username == '')
//    {$('.name_input').next().html('用户名不能为空');$('.name_input').next().show();error_uname=true;}
//
//    else{$.get('/checkUname/','uname='+username,
//    function(data){
//    if(data.data == 1){error_uname=false;$('.name_input').next().hide();}
//    else{error_uname=true;$('.name_input').next().html('用户名不存在');$('.name_input').next().show();}
//    });}
//}
//
//var error_uname = true;
//
//$('.name_input').blur(function(){
//    check_uname();
//})
//
//$('#login_form').submit(function(){
//    check_uname();
//    if(error_uname == false){
//        return true;
//    }
//    else{return false;}
//})
var error_catcode = true;
function changeCode(){$('.cat_but img').attr('src',$('.cat_but img').attr('src')+1);}
function check_code(){
    var user_code = $('.cat_input').val();
    if(user_code == ''){
            error_catcode = true;
            $('.cat_error').html('请输入验证码');
            $('.cat_error').css('color','red');
            $('.cat_error').show();
        }
    else{
    $.get('/loginVerifyTest/','user_code='+user_code,function(data){
        if(data == 1){
            error_catcode = false;
            $('.cat_error').html('验证码正确');
            $('.cat_error').css('color','green');
            $('.cat_error').show();
        }
        else{
            error_catcode = true;
            $('.cat_error').html('验证码错误');
            $('.cat_error').css('color','red');
            $('.cat_error').show();
        }
    });}
    }
$(function(){
    $('.cat_but').click(function(){changeCode();})
    $('.cat_input').change(function(){check_code();})
    $('.login_form').submit(function(){
        if(error_catcode == false){return true;}
        else{return false;}
    });


    })