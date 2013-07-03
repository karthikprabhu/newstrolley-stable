from django.db import models

from newsreader.models import Source
from newstrolley.utils import get_object_or_none

from taggit.models import Tag
from taggit.managers import TaggableManager
from tags import blue_mystic as bm

import logging
logger = logging.getLogger(__name__)

class Article(models.Model):
	pub_date = models.DateTimeField(max_length=60, null=True)
	link = models.URLField()
	source = models.ForeignKey(Source)

	heading = models.CharField(max_length=128)
	summary = models.TextField()
	body = models.TextField(null=True)

	tags = TaggableManager(blank=True)

	stored_datetime = models.DateTimeField(auto_now_add=True)

	def add_tag(self, tag_name):
		'''
		Adds a tag to this article. If the tag already exists, it adds the tag to this article 
		'''
		tag = tag_name.strip().lower()
		db_tag = get_object_or_none(Tag, name=tag_name)
		if db_tag is not None:
			tag = db_tag
		self.tags.add(tag)

	def tag_self(self):
		'''
		Automatically generates tags for this article
		'''
		logger.debug("Generating new tags for article " + self.get_heading())
		tags = bm.get_tags(self.link)
		for tag in tags:
			self.add_tag(tag)
		logger.info("The following tags were added to " + self.get_heading() + " : " + str(tags))

	def __str__(self):
		return self.source.name + " => " + self.heading

	def __unicode__(self):
		return self.source.name + " => " + self.heading

	def get_heading(self):
		return u''.join(self.heading).encode('utf-8').strip()

	def get_summary(self):
		return u''.join(self.summary).encode('utf-8').strip()