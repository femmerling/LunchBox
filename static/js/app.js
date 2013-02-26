$(document).ready(function(){

	function displayNotification(message){
		$('#notify-msg').html(message);
		window_height = $(window).height();
		window_width = $(window).width();
		left_position = (window_width - 370) / 2;
		top_position = (window_height - 150) / 2;
		console.log(left_position);
		console.log(top_position);
		$('#notification-space').css("top",top_position);
		$('#notification-space').css("left",left_position);
		$('#spotlight').show()
		$('#notification-space').show()
	}	
	
	$('#submitReg').click(function(e){
		e.preventDefault();
		if($('[type=text]').val()=="" || $('[type=password]').val()==""){
			displayNotification("Please fill all the fields to register!");
		}else{
			if($('[name=password]').val()!=$('[name=confirm]').val()){
				displayNotification("Password and confirmation did not match");
				$('[name=password]').focus();	
			}else{
				$('#user_add').submit();
			}
		}
	});

	$('#submitLogin').click(function(e){
		e.preventDefault();
		if($('[type=text]').val()=="" || $('[type=password]').val()==""){
			displayNotification("Please fill username and password to login!");
		}else{
			$('#login_form').submit();
		}
	});

	$('#submitPayFriend').click(function(e){
		e.preventDefault();
		if($('[type=text]').val()==""){
			displayNotification("Please fill all the fields");
		}else{
			$('#pay_friend').submit();
		}
	});

	$('#submitTrans').click(function(e){
		e.preventDefault();
		if($('[type=text]').val()==""){
			displayNotification("Please fill all the fields");
		}else{
			$('#transactions_add').submit();
		}
	});

	$('#submitPayTo').click(function(e){
		e.preventDefault();
		if($('[type=text]').val()==""){
			displayNotification("Please fill all the fields");
		}else{
			$('#transactions_pay').submit();
		}
	});	

	$('#popClose').click(function(e){
		e.preventDefault();
		$('#spotlight').hide()
		$('#notification-space').hide()
	});
});