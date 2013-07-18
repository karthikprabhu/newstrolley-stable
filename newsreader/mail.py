from django.core.mail import send_mail

def send_confirmation_mail(name, email, token):
	'''
	Sends email verification mail
	'''
	subject = 'Welcome to NewsTrolley'
	from_mail = 'NewsTrolley <support@newstrolley.com>'
	content_start = 'Hello %s,\n' % str(name)

	content_p1 = ('Thank you for signing up at NewsTrolley. '
	'We are really pleased to have you on board with us. '
	'We hope that your custom newspaper at NewsTrolley will become an essential part of your morning tea and newspaper ritual. '
	'Make sure you have followed your favorite topics so you receive the news that matters.\n')
	
	content_p2 = ('In order for us to serve you better we need to verify that this is indeed your email address. '
	'Please click on the following confirmation link to verify your e-mail address:\n')

	content_p3 = 'http://www.newstrolley.com/confirm-email/?email=%s&token=%s\n' % (str(email), str(token))

	content_p4 = 'If you have any questions or need any other assistance, head over to the help center on the website.\n'

	content_end = ('Best wishes,\n' +
	'The NewsTrolley Team\n')

	content = content_start + '\n' + content_p1 + '\n' + content_p2 + '\n' + content_p3 + '\n' + content_p4 + '\n' + content_end

	send_mail(
		subject, 
		content,
		from_mail,
		[email],
		fail_silently=True
	)

def send_reset_password_mail(name, email, token):
	'''
	Sends email containing password reset instructions
	'''
	subject = 'Password reset instructions'
	from_mail = 'NewsTrolley <support@newstrolley.com>'
	content_start = 'Hello %s,\n' % str(name)

	content_p1 = ('We just received a request to reset your account password. '
		'If you made this request, then just follow the instructions below. '
		'In case you did not make the request, you can safely ignore this mail.\n'
	)

	content_p2 = ('Resetting your account password is really simple. '
		'Just click on the link below and you will be presented with a form to enter a new password. That\'s it!\n')

	content_p3 = 'http://www.newstrolley.com/reset-password/?email=%s&token=%s\n' % (str(email), str(token))

	content_p4 = ('We hope you didn\'t have any problems resetting your password. '
		'If you have any questions or need any assistance, just head over to the help center on the website.\n')

	content_end = ('Best wishes,\n'
		'The NewsTrolley Team\n')

	content = content_start + '\n' + content_p1 + '\n' + content_p2 + '\n' + content_p3 + '\n' + content_p4 + '\n' + content_end

	send_mail(
		subject,
		from_mail,
		content,
		[email],
		fail_silently=True
	)