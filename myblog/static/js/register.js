


function getCookie(){
    var r = document.cookie.match('\\b'+name+'=([^;]*)\\b');
    return r?r[1]:undefined;
}


function changeCode(){$('.piccatbut img').attr('src',$('.piccatbut img').attr('src')+1);}
$(function(){

    $('.piccatbut img').click(function(){
    changeCode();
    })


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
        if(data.data == 1){
        $('#user_name').next().html('用户名已存在');
        $('#user_name').next().show();
        error_name = true;
        }
        else{;}
    });}

}



	var error_name = true;
	var error_password = true;
	var error_check_password = true;
	var error_email = true;
	var error_check = false;
	var error_piccatcode = true;
	var error_emailcode = true;


	$('#user_name').blur(function() {

		check_user_name();
		check_uname();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});

	$('#piccatcode').blur(function(){
	    check_piccatcode();
	});

	$('#catcode').blur(function(){
	    check_catcode();
	})










	$('.catbut').click(function(){
	   if(error_piccatcode == false && error_name == false && error_password == false
	   && error_check_password == false && error_email == false && error_check == false)
        {
        var addr = $('#email').val();
        $.get('/sendCode/','mailAddr=' + addr,function(data){
        if(data == 1){
        $('.catbut').next().html('验证码已经发送到您的邮箱');
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
	})

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});


	function check_user_name(){
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名')
			$('#user_name').next().show();
			error_name = true;
		}
		else
		{
			$('#user_name').next().hide();
			error_name = false;
		}
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

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确');
			$('#email').next().show();
			error_check_password = true;
		}

	}


	function check_piccatcode(){
	    var userStr = $('#piccatcode').val();
	    $.get('/verifyTest/','piccatcode='+userStr,function(data){
	        if(data==1){
	        $('.piccatbut').next().html('你输入的验证码正确');
	        $('.piccatbut').next().css('color','green');
	        $('.piccatbut').next().show();
	        error_piccatcode=false;
	        }
	        else{
	        error_piccatcode=true;
	        $('.piccatbut').next().html('你输入的验证码错误');
	        $('.piccatbut').next().css('color','#e62e2e');
			$('.piccatbut').next().show();
			changeCode();
	        }
	    });
	}

    $('#user_name').focus(function(){$(this).next().hide();})
    $('#pwd').focus(function(){$(this).next().hide();})
    $('#cpwd').focus(function(){$(this).next().hide();})
    $('#email').focus(function(){$(this).next().hide();})
    $('#piccatcode').focus(function(){$(this).next().next().hide();})
    $('#catcode').focus(function(){$(this).next().next().hide();})



    function check_catcode(){
        var userCode = $('#catcode').val();
        $.get('/checkMailCode/','mailCode='+userCode,function(data){
            if(data == 1){
            error_emailcode=false;
            }
            else{
            error_emailcode=true;
            $('.catbut').next().html('验证码错误');
            $('.catbut').next().css('color','red');
			$('.catbut').next().show();
            }
        });
    }








	$('#reg_form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();
		check_piccatcode();
		check_catcode();


		if(error_emailcode == false && error_piccatcode == false && error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});

})