from django.db import models
from django.db import IntegrityError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import NTUser
from newstrolley.utils import get_object_or_none
from newsreader import mail

from PIL import Image
from cStringIO import StringIO
from taggit.managers import TaggableManager

import logging
logger = logging.getLogger(__name__)

class TabManager(models.manager.Manager):
	'''
	Manager for tab operations
	'''
	def create_tab(self, user, name, image=None, **extra_fields):
		'''
		Determines the order number and makes sure the tab is unique to the user
		'''
		image_size_exceeded = False
		order = len(Tab.objects.filter(user=user)) + 1
		
		#If the user is not logged in or the tab name is not specified
		if not user or not name:
			raise ValueError("Tab name must be specified")

		#Make sure the image size is less than 1MB
		if image and image.size >= 1024*1024:
			image = None
			image_size_exceeded = True
		
		#Check if the tab already exists
		try:
			Tab.objects.get(user=user, name=name)
		except Tab.DoesNotExist, e:
			#Insert into the database if tab does not exist
			tab = self.model(user=user, name=name, order=order, image=image)
			tab.save(self._db)

			if image_size_exceeded:
				raise ValueError("Image size exceeded 1MB limit")
			elif image:
				self.resize_image(tab.image, (64, 64))

			return tab

		raise IntegrityError("Tab already exists")

	def resize_image(self, image, size):
		'''
		Resizes the image to the specified size
		'''
		logger.debug("Resizing image %s" % str(image))

		img = Image.open(open(image.file.name, 'rb'))
		img.thumbnail(size, Image.ANTIALIAS)
		outfile = open(image.file.name, 'w+b')
		img.save(outfile, img.format)
		outfile.close()
		
		logger.debug("Image %s resized to %s" % (str(image), str(size)))

class Source(models.Model):
	'''
	Represents a news source
	'''
	name = models.CharField(max_length=60)
	link = models.URLField(unique=True)
	last_update = models.DateTimeField(max_length=60, null=True)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

class Tab(models.Model):
	'''
	Represents a user's tab
	'''
	user = models.ForeignKey(NTUser)

	name = models.CharField(max_length=30)
	order = models.IntegerField()
	image = models.ImageField(upload_to='tab_thumbs/', blank=True)

	tags = TaggableManager(blank=True)

	objects = TabManager()

	def __str__(self):
		return str(self.user.name) + ' - ' + self.name + '(' + str(self.order) + ')'

	def __unicode__(self):
		return str(self.user.name) + ' - ' + self.name + '(' + str(self.order) + ')'

	def add_source(self, source):
		'''
		Adds a new source to this tab and automatically assigns the lowest priority. Returns None if source already exists
		'''
		if source:
			priority = len(TabSource.objects.filter(tab=self)) + 1
			logger.debug("New priority=%s" % str(priority))
			try:
				TabSource.objects.get(tab=self, source=source)
			except TabSource.DoesNotExist:
				TabSource.objects.create(tab=self, source=source, source_priority=priority)
				self.clear_cache()
				return source

		return None

	def get_sources(self):
		'''
		Returns a list of sources ordered according to their priority
		'''
		return [tabsource.source for tabsource in TabSource.objects.filter(tab=self).order_by('source_priority')]

	def change_source_priority(self, source, priority):
		'''
		Changes the priority of the source to the specified priority. Returns the new priority is successful, None if unsuccessful
		'''
		tabsource = get_object_or_none(TabSource, tab=self, source=source)
		if tabsource:
			tabsource = tabsource.change_priority(priority)
			self.clear_cache()
		return tabsource

	def delete_source(self, source):
		'''
		Assigns the last priority to the source and then deletes it.
		'''
		#Get the last priority
		priority = len(TabSource.objects.filter(tab=self))
		logger.debug("Last priority=%s" % str(priority))
		if self.change_source_priority(source, priority):
			logger.debug("Priority set. Deleting source")
			TabSource.objects.get(tab=self, source=source).delete()
			self.clear_cache()
			return source
		return None

	def change_order(self, order):
		'''
		Changes the order of this tab and automatically reorders the rest
		'''
		if self.order == order or order > len(Tab.objects.filter(user=self.user)) or order == 0:
			return self.order
		
		logger.debug("Changing tab(%s) order to %s" % (str(self), str(order)))
		
		tabs = Tab.objects.filter(user=self.user).order_by('order')
		op = 1 if self.order > order else -1
		
		logger.debug("Re-ordering other tabs(op=%s)" % str(op))
		
		for index in range(order, self.order, op):
			tab = tabs[index - 1]
			tab.order += op
			tab.save()
		
		logger.debug("Re-ordered other tabs")
		
		self.order = order
		self.save()
		
		logger.debug("Order changed successfuly")
		return self.order

	def add_tag(self, tag):
		'''
		Adds a new tag to this tab. Clears the cache after adding
		'''
		if tag:
			self.tags.add(tag)
			logger.debug("Added new tag %s to tab %s" % (str(tag), str(self)))
		self.clear_cache()

	def delete_tag(self, tag):
		'''
		Deletes a tag from this tab and clears the cache after
		'''
		if tag:
			self.tags.remove(tag)
			logger.debug("Deleted tag %s from tab %s" % (str(tag), str(self)))
		self.clear_cache()

	def clear_cache(self):
		'''
		Clears the cache associated with this tab
		'''
		cache_key = str(self.user.id) + str(self.id)
		logger.debug("Deleting cache for tab %s. (cache_key=%s)" % (str(self), str(cache_key)))
		cache.delete(cache_key)

class TabSource(models.Model):
	'''
	Associates a tab with the respective sources
	'''
	source = models.ForeignKey(Source)
	tab = models.ForeignKey(Tab)

	source_priority = models.IntegerField()

	def __str__(self):
		return self.tab.name + ' - ' + self.source.name + '(' + str(self.source_priority) + ')'

	def __unicode__(self):
		return self.tab.name + ' - ' + self.source.name + '(' + str(self.source_priority) + ')'

	def change_priority(self, priority):
		if self.source_priority == priority or priority > len(TabSource.objects.filter(tab=self.tab)) or priority == 0:
			return self.source_priority
		
		logger.debug("Changing source(%s) priority to %s" % (str(self.source), str(priority)))
		
		tabsources = TabSource.objects.filter(tab=self.tab).order_by('source_priority')
		op = 1 if self.source_priority > priority else -1
		
		logger.debug("Re-ordering other sources(op=%s)" % str(op))
		for index in range(priority, self.source_priority, op):
			tabsource = tabsources[index - 1]
			tabsource.source_priority += op
			tabsource.save()
		logger.debug("Other sources re-ordered")
		self.source_priority = priority
		self.save()
		logger.debug("Priority changed successfuly")

		return self.source_priority

@receiver(post_save, sender=NTUser)
def default_tabs(sender, **kwargs):
	user = kwargs.get('instance', None)
	created = kwargs.get('created', None)

	#If it was a newly created record
	if created and user:
		#Create default tab
		logger.debug("Creating default tabs for user %s" % str(user))
		tab = Tab.objects.create_tab(user=user, name='Headlines')
		source = get_object_or_none(Source, name='CNN-IBN Top Stories')
		if source:
			tab.add_source(source)
			logger.debug("Default tab created successfuly")

		logger.debug("Sending confirmation email to user %s" % str(user))
		token = user.get_email_confirmation_token()
		mail.send_confirmation_mail(str(user.name), str(user.email), str(token))
		logger.debug("Mail sent to %s" % str(user.email))