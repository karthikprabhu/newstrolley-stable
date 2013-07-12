$(document).ready(function(){
	$("#signup-login").click(function(){
		$('#signup-form-modal').modal('hide');
		$('#login-modal').modal('show');
	});

	function register(id, regex, message) {
		$(id).tooltip({
			'placement': 'right',
			'title': message,
			'container': '#signup-form-modal',
			'trigger': 'manual'
		});
		var validate = function () {
			if($(id).val().match(regex)) {
				if($(id).parent().hasClass("error") || !$(id).parent().hasClass("success")) {
					$(id).parent().removeClass("error");
					$(id).parent().addClass("success");
					$(id).tooltip("hide");
					$(id).focus();
				}
				$(id).next().css("background", "url('/static/newsreader/media/success.png') no-repeat center");
			}
			else {
				if($(id).parent().hasClass("success") || !$(id).parent().hasClass("error")) {
					$(id).parent().removeClass("success");
					$(id).parent().addClass("error");
					$(id).tooltip("show");
				}
				$(id).next().css("background", "url('/static/newsreader/media/error.png') no-repeat center");
			}
		}
		
		$(id).focus(function() {
			setInterval(validate, 100);
		});
	}
	
	var email_regex = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
	register("#email", email_regex, "Enter a valid e-mail address");

	var name_regex = /^[a-zA-Z-']+(\ [a-zA-Z-']+)?$/;
	register("#name", name_regex, "Enter alphanumeric characters only");

	var password_regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
	register("#password", password_regex, "Password should contain a lowercase letter, an uppercase letter and a digit");

	function retype_password() {
		if($("#password").val() == $("#rpassword").val()) {
			if($("#rpassword").parent().hasClass("error") || !$("#rpassword").parent().hasClass("success")) {
				$("#rpassword").parent().removeClass("error");
				$("#rpassword").parent().addClass("success");
				$("#rpassword").tooltip("hide");
				$("#rpassword").focus();
			}
			$("#rpassword").next().css("background", "url('/static/newsreader/media/success.png') no-repeat center");
		}
		else {
			if($("#rpassword").parent().hasClass("success") || !$("#rpassword").parent().hasClass("error")) {
				$("#rpassword").parent().removeClass("success");
				$("#rpassword").parent().addClass("error");
				$("#rpassword").tooltip("show");
			}
			$("#rpassword").next().css("background", "url('/static/newsreader/media/error.png') no-repeat center");
		}
	}
	$("#rpassword").tooltip({
		'placement': 'right',
		'title': "Passwords do not match",
		'container': '#signup-form-modal',
		'trigger': 'manual'
	});
	
	$("#rpassword").focus(function(){
		setInterval(retype_password, 100);
	});

	function form_validate() {
		if($("#email").parent().hasClass("success") && $("#name").parent().hasClass("success") && $("#password").parent().hasClass("success") && $("#rpassword").parent().hasClass("success")) {
			$("#create-account").removeClass("disabled");
			return true;
		}
		else
			$("#create-account").addClass("disabled");
		return false;
	}
	setInterval(form_validate, 100);
	$("#signup-form").submit(form_validate);
});
