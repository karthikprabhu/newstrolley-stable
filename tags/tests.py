from django.test import TestCase

from newsreader.tests import testdb
from newsreader.tests.ajaxutils import dajaxice_get, dajaxice_post

import json

class AjaxTest(TestCase):
	def setUp(self):
		testdb.setup_db(self)

		#Add tags to the 1st tab
		self.tags = ["india", "technology", "world", "international", "politics"]
		for tag in self.tags:
			self.tabs[0].tags.add(tag)

	def test_add_tag(self):
		'''
		add_tag must add a new tag to the tab.
		'''
		#Anonymous user
		response = dajaxice_post(self.client, 'tags', 'add_tag', {'tab_id': self.tabs[0].id, 'tag': 'lifestyle'})
		self.assertFalse(json.loads(response.content)['success'])
		
		#Logged in user
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_post(self.client, 'tags', 'add_tag', {'tab_id': self.tabs[0].id, 'tag': 'lifestyle'})
		self.assertTrue(json.loads(response.content)['success'])

		#Invalid tab id
		response = dajaxice_post(self.client, 'tags', 'add_tag', {'tab_id': 100, 'tag': 'lifestyle'})
		self.assertFalse(json.loads(response.content)['success'])

	def test_delete_tag(self):
		'''
		delete_tag must delete a valid tag
		'''
		#Anonymous user
		response = dajaxice_post(self.client, 'tags', 'delete_tag', {'tab_id': self.tabs[0].id, 'tag': self.tags[0]})
		self.assertFalse(json.loads(response.content)['success'])

		#Logged in user
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_post(self.client, 'tags', 'delete_tag', {'tab_id': self.tabs[0].id, 'tag': self.tags[0]})
		self.assertTrue(json.loads(response.content)['success'])

		#Invalid tab id
		response = dajaxice_post(self.client, 'tags', 'delete_tag', {'tab_id': 100, 'tag': self.tags[0]})
		self.assertFalse(json.loads(response.content)['success'])

		#Un-associated tag
		response = dajaxice_post(self.client, 'tags', 'delete_tag', {'tab_id': 100, 'tag': 'lifestyle'})
		self.assertFalse(json.loads(response.content)['success'])

	def test_get_tags(self):
		'''
		get_tags must return a list of tags matching the query
		'''
		#Valid query
		response = dajaxice_get(self.client, 'tags', 'get_tags', {'query': 'nat'})
		self.assertEqual(json.loads(response.content)['tags'], [self.tags[3]])

		#Invalid query
		response = dajaxice_get(self.client, 'tags', 'get_tags', {'query': 'Habababa'})
		self.assertEqual(json.loads(response.content)['tags'], [])

		#Empty query should return empty list
		response = dajaxice_get(self.client, 'tags', 'get_tags', {'query': ''})
		self.assertEqual(json.loads(response.content)['tags'], [])

	def test_get_tab_tags(self):
		'''
		get_tab_tags must return the tags associated with a tab
		'''
		#Anonymous user
		response = dajaxice_get(self.client, 'tags', 'get_tab_tags', {'tab_id': self.tabs[0].id})
		self.assertEqual(json.loads(response.content)['tags'], [])

		#Logged in user
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_get(self.client, 'tags', 'get_tab_tags', {'tab_id': self.tabs[0].id})
		self.assertEqual(json.loads(response.content)['tags'], self.tags)

		#Invalid tab id
		response = dajaxice_get(self.client, 'tags', 'get_tab_tags', {'tab_id': 100})
		self.assertEquals(json.loads(response.content)['tags'], [])