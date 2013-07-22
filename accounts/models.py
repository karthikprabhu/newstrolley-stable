from django.db import models
from django.contrib.auth.models import BaseUserManager, UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import validate_email
from django.conf import settings
from django.core.cache import cache

import hashlib
import os

class NTUserManager(BaseUserManager):
	#Adds a new user to the database. superuser value determines if the user is a superuser or not
	def create_user(self, name, email, password, superuser=False, **extra_fields):
		now = timezone.now()
		
		#Required fields
		if not name or not email or not password:
			raise ValueError('Name, Email or Password cannot be empty')

		#Normalize and validate email
		email = UserManager.normalize_email(email)
		validate_email(email)

		user = self.model(name=name, email=email, is_active=True, is_staff=superuser, is_superuser=superuser, last_login=now, **extra_fields)
		user.set_password(password)
		
		user.save(using=self._db)
		
		return user

	#Creates a superuser. Django auth requires this method to be implemented
	def create_superuser(self, email, password, name='Superuser', **extra_fields):
		return self.create_user(name, email, password, True)

class NTUser(AbstractBaseUser, PermissionsMixin):
	name = models.CharField('name', max_length=30, unique=False, db_index=True)
	email = models.EmailField('email address', max_length=254, unique=True)
	newspaper_name = models.CharField('newspaper name', max_length=128, default='NewsTrolley')
	
	objects = NTUserManager()
	
	USERNAME_FIELD = 'email'
	
	is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')
	is_active = models.BooleanField('active', default=False,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')

	verified = models.BooleanField('email verified', default=False)
	
	def get_short_name(self):
		return ''

	def get_email_confirmation_token(self):
		message = str(self.id) + str(self.name) + str(self.email) + str(settings.SECRET_KEY)
		m = hashlib.md5()
		m.update(message)
		return m.hexdigest()

	def generate_password_reset_token(self):
		cache_key = str(self.id) + "reset_password"
		token = os.urandom(24).encode('hex')
		expires = 6 * 60 * 60 #6 hours

		self.delete_password_reset_token()
		cache.add(cache_key, token, expires)

		return token

	def get_password_reset_token(self):
		cache_key = str(self.id) + "reset_password"
		return cache.get(cache_key, None)

	def delete_password_reset_token(self):
		cache_key = str(self.id) + "reset_password"
		cache.delete(cache_key)