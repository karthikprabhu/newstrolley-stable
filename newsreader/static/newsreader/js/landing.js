$( document ).ready(function() {
	$( "#signup-login" ).click(function(){
		$( "#signup-form-modal" ).modal( "hide" );
		$( "#login-modal" ).modal( "show" );
	});

	$.fn.validate.defaults.validClass = "success";
	$.fn.validate.defaults.invalidClass = "error";
	
	$( "#name" ).validate({
		condition: /^[a-zA-Z-']+(\ [a-zA-Z-']+)?$/,
		invalidHelper: "Invalid chaaracters in name",
		validHelper: "Nice to meet you."
	});

	$( "#email" ).validate({
		condition: "email",
		invalidHelper: "Enter a valid email address",
		validHelper: "We promise we will not spam you!"
	});

	$( "#password" ).validate({
		condition: "password",
		invalidHelper: "Password must contain atleast 1 uppercase letter and 1 number",
	});

	$( "#rpassword" ).validate({
		condition: function( value ) {
			return value == $( "#password" ).val();
		},
		invalidHelper: "Passwords do not match"
	});

	$( "#signup-form" ).validate({});
});