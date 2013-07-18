from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.staticfiles import finders

import testdb

class ViewsTest(TestCase):
	'''
	-------------------------
	Landing page tests
	-------------------------
	'''
	def setUp(self):
		'''
		Setup database for testing
		'''
		testdb.setup_db(self)
	
	def test_landing_page_status(self):
		'''
		Verifies the landing page is working and the correct template is rendered.
		All context parameters should be None by default
		'''
		response = self.client.get(reverse('newsreader:index'))
		self.assertEqual(response.status_code, 200)
		self.assertTrue('newsreader/index.html' in [template.name for template in response.templates])
		self.assertFalse(response.context['login_error'] or response.context['user_exists'] or response.context['email'])
	
	def test_landing_page_context_parameters(self):
		'''
		GET parameters should be passed into the context
		'''
		response = self.client.get(reverse('newsreader:index'), {'login_error': 1, 'user_exists': 1, 'email': 'karthik@kp.com'})
		self.assertEqual(response.context['login_error'], '1')
		self.assertEqual(response.context['user_exists'], '1')
		self.assertEqual(response.context['email'], 'karthik@kp.com')

	def test_landing_page_logged_in_user(self):
		'''
		A logged in user must redirected to the home page
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		response = self.client.get(reverse('newsreader:index'))
		self.assertEqual(response.get('Location'), self.home_page_url)

	'''
	-------------------------
	Home page tests
	-------------------------
	'''
	def test_home_page_anonymous_user(self):
		'''
		Anonymous users should be redirected to the landing page
		'''
		response = self.client.get(reverse('newsreader:home'))
		self.assertEqual(response.get('Location'), self.landing_page_url)

	def test_home_page_logged_in_user(self):
		'''
		Home page template should be rendered for logged in users and context should contain the necessary information
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		
		response = self.client.get(reverse('newsreader:home'))
		self.assertEqual(response.status_code, 200)
		
		#Verify correct template is rendered
		self.assertTrue('newsreader/home.html' in [template.name for template in response.templates])

		#context['tabs'] should contain the tabs in ascending order of order number
		tab_ids = [tab.id for tab in self.tabs]
		context_tab_ids = [tab.id for tab in response.context['tabs']]
		self.assertEqual(tab_ids, context_tab_ids)

		#context['active_tab'] must be equal to first tab since no tab_id parameter is passed
		self.assertEqual(response.context['active_tab'], self.tabs[0])

		#GET parameters in the context should be None
		self.assertEqual(response.context['image_size_exceeded'], None)
		self.assertEqual(response.context['tab_already_exists'], None)

	def test_home_page_tab_id_parameter(self):
		'''
		context['active_tab'] must be the tab_id when valid tab_id is passed and result in 404 error when invalid tab_id is passed
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		response = self.client.get(reverse('newsreader:home', kwargs={'tab_id': self.tabs[1].id}))
		self.assertEqual(response.context['active_tab'], self.tabs[1])

		#Incorrect tab_id should result in a 404 error
		response = self.client.get(reverse('newsreader:home', kwargs={'tab_id': 1234}))
		self.assertEqual(response.status_code, 404)

	def test_home_page_get_parameters(self):
		'''
		Valid GET parameters must be passed into the context
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		response = self.client.get(reverse('newsreader:home'), {'image_size_exceeded': 1, 'tab_already_exists': 'Hello'})
		self.assertEqual(response.context['image_size_exceeded'], '1')
		self.assertEqual(response.context['tab_already_exists'], 'Hello')

	'''
	-------------------------
	Login view tests
	-------------------------
	'''
	def test_login_with_incorrect_credentials(self):
		'''
		Users must be redirected to login_error_url when email or password is incorrect
		'''
		response = self.client.post(reverse('newsreader:login'), {'email': self.user_email, 'password': 'Habababa'})
		self.assertEqual(response.get('Location'), self.login_error_url)

	def test_login_with_correct_credentials(self):
		'''
		Users must be redirected to the home page when the credentials are correct
		'''
		response = self.client.post(reverse('newsreader:login'), {'email': self.user_email, 'password': self.user_pass})
		self.assertEqual(response.get('Location'), self.home_page_url)

	def test_login_with_missing_parameters(self):
		'''
		Users must be redirected to login_error_url when any of the parameters are missing
		'''
		#no parameters
		response = self.client.post(reverse('newsreader:login'))
		self.assertEqual(response.get('Location'), self.login_error_url)

		#only email
		response = self.client.post(reverse('newsreader:login'), {'email': self.user_email})
		self.assertEqual(response.get('Location'), self.login_error_url)

		#only password
		response = self.client.post(reverse('newsreader:login'), {'password': 'Habababa'})
		self.assertEqual(response.get('Location'), self.login_error_url)

	def test_login_with_get_request(self):
		'''
		A GET request must be redirected to login_error_url
		'''
		response = self.client.get(reverse('newsreader:login'), {'email': self.user_email, 'password': self.user_pass})
		self.assertEqual(response.get('Location'), self.login_error_url)

	def test_login_with_logged_in_user(self):
		'''
		When user is already logged in, login request must be redirected to the home page
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		response = self.client.post(reverse('newsreader:login'), {'email': self.user_email, 'password': self.user_pass})
		self.assertEqual(response.get('Location'), self.home_page_url)

	'''
	-------------------------
	Signup tests
	-------------------------
	'''

	def test_signup_with_missing_parameters(self):
		'''
		Signup request with missing parameters must be redirected to the landing page
		'''
		parameters_list = [
			{},
			{'name': self.user_name}, 
			{'email': self.user_email}, 
			{'password': self.user_pass}, 
			{'name': self.user_name, 'email': self.user_email},
			{'name': self.user_name, 'password': self.user_pass},
			{'email': self.user_email, 'password': self.user_pass},
		]
		
		for parameters in parameters_list:
			response = self.client.post(reverse('newsreader:signup'), parameters)
			self.assertEqual(response.get('Location'), self.landing_page_url)

	def test_signup_with_all_parameters(self):
		'''
		Signup request with all parameters must be redirected to the home page
		'''
		response = self.client.post(reverse('newsreader:signup'), {'name': self.user_name, 'email': 'k_karthikp@gmail.com', 'password': 'Habababa'})
		self.assertEqual(response.get('Location'), self.home_page_url)

	def test_signup_with_already_existing_email(self):
		'''
		Signup request with already existing email must be redirected to landing page with the correct GET parameters
		'''
		response = self.client.post(reverse('newsreader:signup'), {'name': self.user_name, 'email': self.user_email, 'password': 'Habababa'})
		self.assertEqual(response.get('Location'), self.landing_page_url + '?user_exists=1&email=%s' % self.user_email)

	def test_signup_with_get_request(self):
		'''
		A GET request must be ignored and the user must be redirected to the landing page
		'''
		response = self.client.get(reverse('newsreader:signup'), {'name': self.user_name, 'email': self.user_email, 'password': 'Habababa'})
		self.assertEqual(response.get('Location'), self.landing_page_url)

	'''
	-------------------------
	Logout view tests
	-------------------------
	'''
	def test_logout_with_logged_in_user(self):
		'''
		User must be logged out and redirected to the landing page
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		response = self.client.get(reverse('newsreader:logout'))
		self.assertEqual(response.get('Location'), self.landing_page_url)

	def test_logout_with_anonymous_user(self):
		'''
		Redirect the anonymous user to the landing page without error
		'''
		response = self.client.get(reverse('newsreader:logout'))
		self.assertEqual(response.get('Location'), self.landing_page_url)

	'''
	-------------------------
	Add tab tests
	-------------------------
	'''
	def test_add_tab_with_small_image(self):
		'''
		Small image must be added and the user must be redirected to the tab 
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		image = open(finders.find('newsreader/media/small_image.jpg'), 'rb')
		response = self.client.post(reverse('newsreader:add_tab'), {'name': 'Small Image', 'image': image})
		image.close()
		self.assertRegexpMatches(response.get('Location'), self.home_page_url + '[0-9]+')

	def test_add_tab_with_large_image(self):
		'''
		When adding a large image, redirect user to home page with image_size_exceeded GET parameter
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		image = open(finders.find('newsreader/media/large_image.jpg'), 'rb')
		response = self.client.post(reverse('newsreader:add_tab'), {'name': 'Large Image', 'image': image})
		image.close()
		self.assertEqual(response.get('Location'), self.home_page_url + '?image_size_exceeded=1')

	def test_add_tab_with_same_name(self):
		'''
		When 2 tabs have the same name, redirect user to home page with tab_already_exists GET parameter
		'''
		self.client.login(email=self.user_email, password=self.user_pass)
		response = self.client.post(reverse('newsreader:add_tab'), {'name': 'Small Image'})
		response = self.client.post(reverse('newsreader:add_tab'), {'name': 'Small Image'})
		self.assertEqual(response.get('Location'), self.home_page_url + '?tab_already_exists=' + 'Small%20Image')

	'''
	-------------------------
	Reset password tests
	-------------------------
	'''
	def test_reset_password_get(self):
		#without parameters it must have default context values
		response = self.client.get(reverse('newsreader:reset_password'))
		self.assertTrue(response.context['form'] and not response.context['verify_token'] and not  response.context['success'])

		#with correct parameters and incorrect token
		response = self.client.get(reverse('newsreader:reset_password'), {'email': self.user_email, 'token': 'bullshit'})
		self.assertTrue(not response.context['form'] and response.context['verify_token'] and not response.context['success'])

		#with correct parameters and token
		response = self.client.get(reverse('newsreader:reset_password'), {'email': self.user_email, 'token': self.user.generate_password_reset_token()})
		self.assertTrue(not response.context['form'] and response.context['verify_token'] and response.context['success'])

		#without token
		response = self.client.get(reverse('newsreader:reset_password'), {'email': self.user_email})
		self.assertTrue(response.context['form'] and not response.context['verify_token'] and not response.context['success'])

	def test_reset_password_post(self):
		#invalid email
		response = self.client.post(reverse('newsreader:reset_password'), {'email': 'hababab@habababa.com'})
		self.assertFalse(response.context['form'] or response.context['verify_token'] or response.context['success'])

		#valid email, unverified user
		response = self.client.post(reverse('newsreader:reset_password'), {'email': self.user_email})
		self.assertFalse(response.context['form'] or response.context['verify_token'] or response.context['success'])

		#valid email, verified user
		self.user.verified = True
		self.user.save()
		response = self.client.post(reverse('newsreader:reset_password'), {'email': self.user_email})
		self.assertFalse(response.context['form'] or response.context['verify_token'] or not response.context['success'])