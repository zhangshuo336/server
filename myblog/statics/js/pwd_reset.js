var error_name = true;
var error_password = true;
var error_check_password = true;
var error_catcode = true;
var error_emailcode=true;
function changeCode(){$('.piccatbut img').attr('src',$('.piccatbut img').attr('src')+1);}
function check_code(){
    var user_code = $('#piccatcode').val();
    if(user_code == ''){
            error_catcode = true;
            $('#verify_error').html('请输入验证码');
            $('#verify_error').css('color','red');
            $('#verify_error').show();
        }
    else{
    $.get('/loginVerifyTest/','user_code='+user_code,function(data){
        if(data == 1){
            error_catcode = false;
            $('#verify_error').html('验证码正确');
            $('#verify_error').css('color','green');
            $('#verify_error').show();
        }
        else{
            error_catcode = true;
            $('#verify_error').html('验证码错误');
            $('#verify_error').css('color','red');
            $('#verify_error').show();
        }
    });}
    }


function check_uname(){
    var uname = $('#user_name').val();

    if(uname == ''){
    $('#user_name').next().html('用户名不能为空');
    $('#user_name').next().show();
    error_name = true;
        }
    else{
    //    判断用户名是否存在
    $.get('/checkUname/','uname='+uname,function(data){
        if(data.data == 0){
        $('#user_name').next().html('用户名不存在');
        $('#user_name').next().show();
        error_name = true;
        }
        else{$('#user_name').next().hide();error_name = false;}
    });}

}


function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}
	}

	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}

	}


function sendMailCode(){
        if(error_name == false && error_password == false && error_check_password == false && error_catcode == false)
        {
        var uname = $('#user_name').val();
        $.get('/pwd_reset_send_code/','uname=' + uname,function(data){
        if(data == 1){
        $('.catbut').next().html('验证码已经发送到邮箱10分钟内有效');
        $('.catbut').next().css('color','green');
        $('.catbut').next().show();
        }
        else{
        $('.catbut').next().html('请核对邮箱是否正确');
        $('.catbut').next().css('color','#e62e2e');
        $('.catbut').next().show();
        }
        });
        }
        else{
        $('.catbut').next().html('请将基本信息填写完全在获取验证码');
        $('.catbut').next().css('color','#e62e2e');
        $('.catbut').next().show();
        }
}


function countDown() {
sendMailCode();
$('.catbut').unbind('click');
var timer = setInterval(function(){
    i = i - 1;
    $('.catbut').html("("+i+"s)");
    $('.catbut').css({'color':'#A7A7A7','backgroundColor':'#D6D6D6','cursor':'default'})
    if (i == 0) {
        clearInterval(timer);
        $('.catbut').html("重新发送");
        $('.catbut').css({'color':'#55991A','backgroundColor':'#f8f8f8','cursor':'pointer'})
        $('.catbut').bind('click',function(){countDown();})
        i = 60;
        return;
    }
    },1000);

}



function check_catcode(){
        var userCode = $('#catcode').val();
        if(userCode == ''){
            error_emailcode=true;
            $('.catbut').next().html('验证码不能为空!');
            $('.catbut').next().css('color','red');
			$('.catbut').next().show();
        }
        else{
        $.get('/pwd_reset_checkmailcode/','mailCode='+userCode,function(data){
            if(data == 1){
            error_emailcode=false;
            $('.catbut').next().html('验证码正确!');
            $('.catbut').next().css('color','green');
			$('.catbut').next().show();
            }
            else{
            error_emailcode=true;
            $('.catbut').next().html('验证码错误');
            $('.catbut').next().css('color','red');
			$('.catbut').next().show();
            }
        });}


    }



var i = 60;
$(function(){


	$('.catbut').click(function(){
//	alert(error_check_password);
//	alert(error_password);
//	alert(error_name);
//	alert(error_catcode);
	if(error_name == false && error_password == false && error_check_password == false && error_catcode == false){
	$('.catbut').next().hide();
        countDown();}
     else{
        $('.catbut').next().html('请将基本信息填写完全在获取验证码');
        $('.catbut').next().css('color','#e62e2e');
        $('.catbut').next().show();
        }
	})

    $('#catcode').keyup(function(){check_catcode();})
    $('#pwd').blur(function() {check_pwd();});
	$('#cpwd').blur(function() {check_cpwd();});
    $('#user_name').keyup(function(){check_uname();});
    $('#user_name').blur(function(){check_uname();});
    $('.piccatbut').click(function(){changeCode();});
    $('#piccatcode').keyup(function(){check_code();});
    $('#reg_form').submit(function(){
        check_uname();
        check_code();
        check_pwd();
        check_cpwd();
        check_catcode();
        if(error_check_password == false && error_catcode == false && error_name == false && error_emailcode == false && error_password == false)
        {return true;}
        else{return false;}
    });

    })

//var error_name = true;
//var error_password = true;
//var error_check_password = true;
//var error_catcode = true;
//error_emailcode=true;