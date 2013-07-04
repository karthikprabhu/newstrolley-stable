from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.cache import cache

from accounts.models import NTUser
from newsreader.models import Tab, Source
from newstrolley.utils import get_object_or_none
from newsreader.tests import testdb
from newsreader.tests.ajaxutils import dajaxice_get, dajaxice_post
from feeds.models import Article

from taggit.models import Tag

from datetime import datetime
from dateutil.tz import tzlocal

import urllib
import json
import feedmanager

class AjaxTest(TestCase):
	'''
	-------------------------
	Basic setup
	-------------------------
	'''
	def setUp(self):
		testdb.setup_db(self)
		self.tabs[2].add_source(self.sources[0])

	'''
	-------------------------
	Test get_article ajax call
	-------------------------
	'''
	def test_get_article(self):
		#Test with anonymous user
		response = dajaxice_get(self.client, 'feeds', 'get_article', {'tab_id': self.tabs[2].id, 'article_no': 1})
		self.assertEqual(json.loads(response.content), {'success': False, 'article': None})

		#Test with logged in user, valid tab
		self.client.login(email='k.karthik.prabhu@gmail.com', password='Dazedanddoped1')
		response = dajaxice_get(self.client, 'feeds', 'get_article', {'tab_id': self.tabs[2].id, 'article_no': 1})
		self.assertEqual(json.loads(response.content).get('success'), True)
		self.assertIsInstance(json.loads(response.content).get('article'), dict)

		#Try retreiving the next article
		response = dajaxice_get(self.client, 'feeds', 'get_article', {'tab_id': self.tabs[2].id, 'article_no': 2})
		self.assertEqual(json.loads(response.content).get('success'), True)
		self.assertIsInstance(json.loads(response.content).get('article'), dict)

class ModelsTest(TestCase):
	def setUp(self):
		testdb.setup_db(self)

		#Create test article
		self.article = Article.objects.create(
			pub_date=datetime.now(tzlocal()), 
			link='http://ibnlive.in.com/news/modi-faces-flak-over-conditions-of-gujarati-muslims-2002-riots/402882-3-238.html',
			source=self.sources[0],
			heading='Sample Article',
			summary='Some stuff in the article',
			body='Some stuff in the article',
		)

	def test_add_tag(self):
		'''
		add_tag must add the tag stirng to the article
		'''
		self.article.add_tag("sample article")
		self.assertEqual([tag.name for tag in self.article.tags.all()], ["sample article"])

		#Add already existing tag
		self.article.add_tag("sample article")
		self.assertEqual([tag.name for tag in self.article.tags.all()], ["sample article"])

	def test_tag_self(self):
		'''
		tag_self should automatically determine tags for the article and add it
		'''
		self.article.tag_self()
		#The selected test article link has been selected so that it does not have 0 tags
		self.assertTrue(len(self.article.tags.all()) > 0)

class FeedManager(TestCase):
	def setUp(self):
		testdb.setup_db(self)
		cache.clear()

	def test_update_feed(self):
		'''
		update_feed should update the list of feeds of a source
		'''
		#First time update. No of updated articles must be greater than 0. CNN-IBN provides 30 articles at once
		articles = feedmanager.update_feed(self.sources[0])
		self.assertEqual(len(articles), 30)

		#Trying to update the source again
		self.assertEqual(len(feedmanager.update_feed(self.sources[0])), 0)

	def test_get_content(self):
		'''
		get_content should retreive the list of articles from different sources in the tab
		'''
		#Invalid tab id
		articles = feedmanager.get_content(user=self.user, tab_id=100)
		self.assertEqual(len(articles), 0)

		#Valid tab id
		self.client.login(email=self.user_email, password=self.user_pass)
		self.tabs[2].add_source(self.sources[0])
		articles = feedmanager.get_content(user=self.user, tab_id=self.tabs[2].id)
		self.assertEqual(len(articles), 30) #Contains only CNN-IBN Top Stories as source. Hence only 30 articles will be retreived

		#Check if articles are filtered by tags
		tag = Tag.objects.all()[0]
		self.tabs[2].add_tag(tag)
		no_of_articles_with_tag = len(Article.objects.filter(source=self.sources[0], tags__in=[tag]))
		articles = feedmanager.get_content(user=self.user, tab_id=self.tabs[2].id)
		self.assertEqual(len(articles), no_of_articles_with_tag)