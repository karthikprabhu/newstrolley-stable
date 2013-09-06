$( document ).ready(function() {
	console.log("@!$!#!@@###############################@@@@@@@@@@@@@@@@@@@@@@@");
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
		condition: function( value ) {
			return value.length >= 6;
		},
		invalidHelper: "Password must contain atleast 6 characters",
	});

	$( "#rpassword" ).validate({
		condition: function( value ) {
			return value.length >= 6 && value == $( "#password" ).val();
		},
		invalidHelper: "Passwords do not match"
	});

	$( "#signup-form" ).validate({});
	
	$( "#new-signup a" ).click(function(){
		$( "#signup-form-modal" ).modal( "show" );
		$( "#login-modal" ).modal( "hide" );
	});
});