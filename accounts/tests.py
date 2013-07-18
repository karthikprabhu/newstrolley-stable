from django.test import TestCase
from django.core.validators import ValidationError
from django.db import IntegrityError
from django.core.cache import cache

from accounts.models import NTUser

class NTUserTests(TestCase):
	'''
	-------------------------
	Test for null or empty parameters
	-------------------------
	'''
	def test_create_user_with_null_parameters(self):
		#When all parameters are None
		self.assertRaises(ValueError, NTUser.objects.create_user, name=None, email=None, password=None)
		
		#When only name is provided
		self.assertRaises(ValueError, NTUser.objects.create_user, name='Karthik', email=None, password=None)

		#When only email is provided
		self.assertRaises(ValueError, NTUser.objects.create_user, name=None, email='k.karthik.prabhu@gmail.com', password=None)

		#When only password is provided
		self.assertRaises(ValueError, NTUser.objects.create_user, name=None, email=None, password='Habababa')
		
		#When name and email are provided
		self.assertRaises(ValueError, NTUser.objects.create_user, name='Karthik', email='k.karthik.prabhu@gmail.com', password=None)

		#When name and password are provided
		self.assertRaises(ValueError, NTUser.objects.create_user, name='Karthik', email=None, password='Habababa')

		#When email and password are provided
		self.assertRaises(ValueError, NTUser.objects.create_user, name=None, email='k.karthik.prabhu@gmail.com', password='Habababa')

		#When name is an empty string
		self.assertRaises(ValueError, NTUser.objects.create_user, name='', email='', password='')

	'''
	-------------------------
	Test for incorrect formats
	-------------------------
	'''
	def test_create_user_with_incorrect_format(self):
		#When invalid email address is provided
		self.assertRaises(ValidationError, NTUser.objects.create_user, name='Karthik', email='Hello,Ladies!!', password='Habababa')

	'''
	-------------------------
	Uniqueness tests
	-------------------------
	'''
	def test_create_user_for_uniqueness(self):
		#When 2 accounts have same email
		user1 = NTUser.objects.create_user(name='Karthik', email='k.karthik.prabhu@gmail.com', password='Hello')
		self.assertRaises(IntegrityError, NTUser.objects.create_user, name='Haba', email='k.karthik.prabhu@gmail.com', password='Habababa')
		
		#When 2 accounts have the same name
		user2 = NTUser.objects.create_user(name='Karthik', email='k_karthikp@outlook.com', password='Habababa')
		self.assertIsInstance(user2, NTUser)

	'''
	-------------------------
	Superuser parameter test
	-------------------------
	'''
	def test_create_user_superuser_parameter(self):
		#When the superuser parameter is not passed
		user = NTUser.objects.create_user(name='Karthik', email='k.karthik.prabhu@gmail.com', password='Habababa')
		self.assertFalse(user.is_staff or user.is_superuser)

		#When superuser parameter is true
		user = NTUser.objects.create_user(name='Karthik', email='kp@kp.com', password='Habababa', superuser=True)
		self.assertTrue(user.is_staff and user.is_superuser)

	'''
	-------------------------
	NTUser methods tests
	-------------------------
	'''
	def test_password_reset_token(self):
		#Generate the token
		user = NTUser.objects.create_user(name='Karthik', email='k.karthik.prabhu@gmail.com', password='Habababa')
		token = user.generate_password_reset_token()

		#Verify the token
		self.assertEqual(token, user.get_password_reset_token())

		#Delete the token and check
		cache_key = str(user.id) + "reset_password"
		cache.delete(cache_key)
		self.assertIsNone(user.get_password_reset_token())