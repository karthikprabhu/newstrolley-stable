from django.test import TestCase

from newsreader.models import Tab
from newstrolley.utils import get_object_or_none

from ajaxutils import dajaxice_get, dajaxice_post

import testdb
import json

class AjaxTests(TestCase):
	def setUp(self):
		testdb.setup_db(self)

	def test_find_sources(self):
		'''
		find_sources should return the sources that matches the given query
		'''
		#Valid query
		response = dajaxice_get(self.client, 'newsreader', 'find_sources', {'query': 'hindu'})
		self.assertEqual(json.loads(response.content), {'names': [self.sources[1].name, self.sources[2].name]})

		#Invalid query
		response = dajaxice_get(self.client, 'newsreader', 'find_sources', {'query': 'Habababa'})
		self.assertEqual(json.loads(response.content), {'names': []})

		#Empty query
		response = dajaxice_get(self.client, 'newsreader', 'find_sources', {'query': ''})
		self.assertEqual(json.loads(response.content), {'names': []})

	def test_get_sources(self):
		'''
		get_sources must return the sources associated with a particular tab. If the tab id is invalid, results must be empty
		'''
		#Empty list must be returned for anonymous user
		response = dajaxice_get(self.client, 'newsreader', 'get_sources', {'tab_id': self.tabs[0].id})
		self.assertEqual(json.loads(response.content), {'sources': []})

		#Valid query must return the sources associated with the tab
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_get(self.client, 'newsreader', 'get_sources', {'tab_id': self.tabs[0].id})
		self.assertEqual(json.loads(response.content), {'sources': [self.sources[0].name, self.sources[1].name, self.sources[2].name]})

		#Invalid tab id must return empty list
		response = dajaxice_get(self.client, 'newsreader', 'get_sources', {'tab_id': 100})
		self.assertEqual(json.loads(response.content), {'sources': []})

		#Tab with empty sources
		response = dajaxice_get(self.client, 'newsreader', 'get_sources', {'tab_id': self.tabs[2].id})
		self.assertEqual(json.loads(response.content), {'sources': []})

	def test_add_source(self):
		'''
		add_source must associate the tab with the source. If the source is already associated with the tab, no error must be thrown
		'''
		#Anonymous user must not be able to add anything
		response = dajaxice_post(self.client, 'newsreader', 'add_source', {'tab_id': self.tabs[2].id, 'source_name': self.sources[0].name})
		self.assertFalse(json.loads(response.content)['success'])

		#Logged in user must be able to associate a valid tab with a valid source
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_post(self.client, 'newsreader', 'add_source', {'tab_id': self.tabs[2].id, 'source_name': self.sources[0].name})
		self.assertTrue(json.loads(response.content)['success'])
		self.assertEqual(self.tabs[2].get_sources(), [self.sources[0]])

		#Invalid tab must not be associated with a source
		response = dajaxice_post(self.client, 'newsreader', 'add_source', {'tab_id': 100, 'source_name': self.sources[1].name})
		self.assertFalse(json.loads(response.content)['success'])

		#Invalid source should not be associated with the tab
		response = dajaxice_post(self.client, 'newsreader', 'add_source', {'tab_id': self.tabs[2].id, 'source_name': 'Habababa'})
		self.assertFalse(json.loads(response.content)['success'])

	def test_remove_source(self):
		'''
		remove_source must delete the source from the tab. Invalid requests must be ignored
		'''
		#Anonymous user test
		response = dajaxice_post(self.client, 'newsreader', 'remove_source', {'tab_id': self.tabs[0].id, 'source_name': self.sources[0].name})
		self.assertFalse(json.loads(response.content)['success'])

		#Logged in user
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_post(self.client, 'newsreader', 'remove_source', {'tab_id': self.tabs[0].id, 'source_name': self.sources[0].name})
		self.assertTrue(json.loads(response.content)['success'])
		self.assertEqual(self.tabs[0].get_sources(), [self.sources[1], self.sources[2]])

		#Invalid tab id
		response = dajaxice_post(self.client, 'newsreader', 'remove_source', {'tab_id': 100, 'source_name': self.sources[0].name})
		self.assertFalse(json.loads(response.content)['success'])

		#Invalid source name
		response = dajaxice_post(self.client, 'newsreader', 'remove_source', {'tab_id': self.tabs[0].id, 'source_name': 'Habababa'})
		self.assertFalse(json.loads(response.content)['success'])

		#Dis-associated source
		response = dajaxice_post(self.client, 'newsreader', 'remove_source', {'tab_id': self.tabs[0].id, 'source_name': self.sources[0].name})
		self.assertFalse(json.loads(response.content)['success'])

	def test_change_source_position(self):
		'''
		change_source_position must change the position of the source
		'''
		#Anonymous user test
		response = dajaxice_post(self.client, 'newsreader', 'change_source_position', {'tab_id': self.tabs[0].id, 'source_name': self.sources[0].name, 'position': 2})
		self.assertFalse(json.loads(response.content)['success'])

		#Logged in user
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_post(self.client, 'newsreader', 'change_source_position', {'tab_id': self.tabs[0].id, 'source_name': self.sources[0].name, 'position': 2})
		self.assertTrue(json.loads(response.content)['success'])
		self.assertEqual(self.tabs[0].get_sources(), [self.sources[1], self.sources[0], self.sources[2]])

		#Invalid tab id
		response = dajaxice_post(self.client, 'newsreader', 'change_source_position', {'tab_id': 100, 'source_name': self.sources[0].name, 'position': 2})
		self.assertFalse(json.loads(response.content)['success'])

		#Invalid source name
		response = dajaxice_post(self.client, 'newsreader', 'change_source_position', {'tab_id': self.tabs[0].id, 'source_name': 'Habababa', 'position': 1})
		self.assertFalse(json.loads(response.content)['success'])

		#Dis-associated source
		response = dajaxice_post(self.client, 'newsreader', 'change_source_position', {'tab_id': self.tabs[0].id, 'source_name': self.sources[4].name, 'position': 1})
		self.assertFalse(json.loads(response.content)['success'])

		#Invalid position
		response = dajaxice_post(self.client, 'newsreader', 'change_source_position', {'tab_id': self.tabs[0].id, 'source_name': self.sources[0].name, 'position': 0})
		self.assertFalse(json.loads(response.content)['success'])
		response = dajaxice_post(self.client, 'newsreader', 'change_source_position', {'tab_id': self.tabs[0].id, 'source_name': self.sources[0].name, 'position': 100})
		self.assertFalse(json.loads(response.content)['success'])

	def test_change_tab_position(self):
		'''
		change_tab_position changes the order of the tabs. Invalid requests must be ignored
		'''
		#Anonymous user test
		response = dajaxice_post(self.client, 'newsreader', 'change_tab_position', {'tab_id': self.tabs[0].id, 'position': 2})
		self.assertFalse(json.loads(response.content)['success'])

		#Logged in user
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_post(self.client, 'newsreader', 'change_tab_position', {'tab_id': self.tabs[0].id, 'position': 2})
		self.assertTrue(json.loads(response.content)['success'])
		self.assertTrue(get_object_or_none(Tab, pk=self.tabs[0].id).order, 2)

		#Invalid tab id
		response = dajaxice_post(self.client, 'newsreader', 'change_tab_position', {'tab_id': 100, 'position': 2})
		self.assertFalse(json.loads(response.content)['success'])

		#Invalid position
		response = dajaxice_post(self.client, 'newsreader', 'change_tab_position', {'tab_id': self.tabs[0].id, 'position': 0})
		self.assertFalse(json.loads(response.content)['success'])
		response = dajaxice_post(self.client, 'newsreader', 'change_tab_position', {'tab_id': self.tabs[0].id, 'position': 100})
		self.assertFalse(json.loads(response.content)['success'])

	def test_delete_tab(self):
		'''
		delete_tab must delete a valid tab. 
		'''
		#Anonymous user test
		response = dajaxice_post(self.client, 'newsreader', 'delete_tab', {'tab_id': self.tabs[0].id})
		self.assertFalse(json.loads(response.content)['success'])

		#Logged in user
		self.client.login(email=self.user_email, password=self.user_pass)
		response = dajaxice_post(self.client, 'newsreader', 'delete_tab', {'tab_id': self.tabs[0].id})
		self.assertTrue(json.loads(response.content)['success'])

		#Invalid tab id
		response = dajaxice_post(self.client, 'newsreader', 'delete_tab', {'tab_id': 100})
		self.assertFalse(json.loads(response.content)['success'])