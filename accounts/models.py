from django.db import models
from django.contrib.auth.models import BaseUserManager, UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import validate_email

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
	
	def get_short_name(self):
		return ''