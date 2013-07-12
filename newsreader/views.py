from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from accounts.models import NTUser
from newsreader.models import Tab

import logging
logger = logging.getLogger(__name__)
'''
--------------------
Landing Page
--------------------
'''
def index(request):
	#If the user is already authenticated, redirect him to the home page
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('newsreader:home'))

	#Pass any GET parameters into the context
	context = {
		'login_error': request.GET.get('login_error', False),
		'user_exists': request.GET.get('user_exists', False),
		'email': request.GET.get('email', None),
	}

	return render(request, 'newsreader/index.html', context)

'''
--------------------
Home Page
--------------------
'''
def home(request, tab_id=None):
	context = {}

	#If user is authenticated, then render the home page
	if request.user.is_authenticated():
		context['tabs'] = Tab.objects.filter(user=request.user).order_by('order')

		if not tab_id:
			if len(context['tabs']) > 0:
				context['active_tab'] = context['tabs'][0]
		else:
			context['active_tab'] = get_object_or_404(Tab, pk=tab_id, user=request.user)

		#Pass any GET parameters into the context
		context.update({
			'image_size_exceeded': request.GET.get('image_size_exceeded', None),
			'tab_already_exists': request.GET.get('tab_already_exists', None),
		})
		return render(request, 'newsreader/home.html', context)
	else:
		#else redirect to the landing/index page
		return HttpResponseRedirect(reverse('newsreader:index'))

'''
--------------------
Account Management
--------------------
'''
def login(request):
	email = request.POST.get('email', None)
	password = request.POST.get('password', None)

	user_ = authenticate(email=email, password=password)
	#If the user credentials are valid, login and redirect to home page
	if user_ is not None:
		auth_login(request, user_)
		return HttpResponseRedirect(reverse('newsreader:home'))

	#If the user credentials are invalid, redirect to home page and show error message
	return HttpResponseRedirect(reverse('newsreader:index') + '?login_error=1')

def signup(request):
	name = request.POST.get('name', None)
	email = request.POST.get('email', None)
	password = request.POST.get('password', None)

	try:
		user = NTUser.objects.create_user(name, email, password, False)
	except IntegrityError, e:
		#If user already exists
		logger.info("User already exists.(name=%s, email=%s)" % (str(name), str(email)))
		return HttpResponseRedirect(reverse('newsreader:index') + '?user_exists=1&email=%s' % email)
	except ValueError, e:
		#If any of the required fields are left empty
		logger.warning("Required fields are left empty. Request=%s" % request)
		return HttpResponseRedirect(reverse('newsreader:index'))

	return login(request)

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect(reverse('newsreader:index'))

def confirm_email(request):
	email = request.GET.get('email', None)
	token = request.GET.get('token', None)
	
	context = {
		'verified': False
	}
	
	if email and token:
		user = get_object_or_404(NTUser, email=email)
		#If the provided token is valid, then activate the account
		if user.get_email_confirmation_token() == token:
			user.verified = True
			user.save()
			context['verified'] = True

	return render(request, 'newsreader/confirm-email.html', context)

'''
-------------------------
Tabs
-------------------------
'''
def add_tab(request):
	error = True
	newtab = None

	if request.method == 'POST' and request.user.is_authenticated():
		image = request.FILES.get('image', None)
		name = request.POST.get('name', None)

		try:
			tab = Tab.objects.create_tab(user=request.user, name=name, image=image)
		except ValueError, e:
			return HttpResponseRedirect(reverse('newsreader:home') + '?image_size_exceeded=1')
		except IntegrityError, e:
			return HttpResponseRedirect(reverse('newsreader:home') + '?tab_already_exists=' + name)

	return HttpResponseRedirect(reverse('newsreader:home', kwargs={'tab_id': tab.id}))