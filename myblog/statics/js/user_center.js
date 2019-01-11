$(function(){
function check_nick_name(){
		var len = $('#nickname').val().length;
		if(len>20 || len<1)
		{
			$('#nick_error').html('昵称不要超过20个字符')
			$('#nick_error').show();
			nick_error = true;
		}
		else
		{
			$('#nick_error').hide();
			nick_error = false;
		}
	}
////===============================================
//var val = $("#test").val();
//var ival = parseInt(val);//如果变量val是字符类型的数则转换为int类型 如果不是则ival为NaN
//    alert(typeof(ival));
//    if(!isNaN(ival)){
//        alert(val +"是数字");
//    } else{
//        alert(val +"不是数字");
//    }
//
////===============================================
	function check_age(){
		var val = $('#age').val();
		var ival = parseInt(val);
		if(!isNaN(ival)){

		if(val>120 || val<1)
		{
			$('#age_error').html('输入符合实际的年龄')
			$('#age_error').show();
			age_error = true;
		}
		else
		{
			$('#age_error').hide();
			age_error = false;
		}
		}
		else{
		    $('#age_error').html('请输入数字!')
			$('#age_error').show();
			age_error = true;
		}




	}







	$('#nickname').focus(function(){
	    $('#nick_error').hide();
			nick_error = false;
	});

	$('#age').focus(function(){
	    $('#age_error').hide();
			age_error = false;
	});

	var nick_error = false;
	var age_error = false;

	$('#usermsg').submit(function() {
		check_age();
		check_nick_name();
		if(nick_error == false && age_error == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});



	})
