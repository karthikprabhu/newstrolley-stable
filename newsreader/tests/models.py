from django.test import TestCase
from django.db import IntegrityError

from accounts.models import NTUser
from newsreader.models import Source, Tab, TabSource
from newstrolley.utils import get_object_or_none

class ModelsTest(TestCase):
	'''
	-------------------------
	Basic setup
	-------------------------
	'''
	def setUp(self):
		self.source = Source.objects.create(name='CNN-IBN Top Stories', link='http://www.ibnlive.com/xml/top.xml')
		self.user = NTUser.objects.create_user(name='Karthik', email='k.karthik.prabhu@gmail.com', password='Dazedanddoped1')
		#A default tab will automatically be created with CNN-IBN Top Stories as the source
		self.tab = get_object_or_none(Tab, user=self.user, name='Headlines')
		if self.tab:
			self.tabsource = get_object_or_none(TabSource, tab=self.tab, source=self.source)

	'''
	-------------------------
	Source model tests
	-------------------------
	'''
	def test_multiple_sources_integrity(self):
		'''
		Verifies that 2 sources does not have the same link
		'''
		#Multiple sources cannot have the same link
		self.assertRaises(IntegrityError, Source.objects.create, name='Hindu', link=self.source.link)
		#Multiple sources may have the same name
		self.assertIsInstance(Source.objects.create(name=self.source.name, link='http://hello.com'), Source)

	'''
	-------------------------
	Tab model tests
	Note: Image test can't be done since it requires an UploadedFile. Image tests are done in views
	-------------------------
	'''
	def test_multiple_tabs_integrity(self):
		'''
		A user must have unique names for each tab. Name can not be left empty
		'''
		#A user must have different names for each tab
		self.assertRaises(IntegrityError, Tab.objects.create_tab, user=self.user, name='Headlines')

		#Different users can have tabs with same names
		user = NTUser.objects.create_user(name='Divyansh', email='divyansh.prakash@yahoo.com', password='Dazedanddoped1')
		tab = get_object_or_none(Tab, user=user, name='Headlines')
		self.assertIsInstance(tab, Tab)

		#ValueError must be raised when trying to create a tab with no name
		self.assertRaises(ValueError, Tab.objects.create_tab, user=self.user, name='')

	def test_order_number(self):
		'''
		Tab order number must automatically increment when new tab is created. Changing the tab order must automatically reorder the rest
		'''
		#Check auto-increment
		tab = Tab.objects.create_tab(user=self.user, name='Hello')
		self.assertEqual(tab.order, 2)

		#Check tab re-order
		self.assertEqual(tab.change_order(1), 1)
		c_tab = get_object_or_none(Tab, pk=self.tab.id) #Retreive the newly changed tab
		self.assertEqual(c_tab.order, 2)

		#Invalid order conditions must result in no change
		self.assertEqual(self.tab.change_order(100), self.tab.order)
		self.assertEqual(self.tab.change_order(0), self.tab.order)

	def test_create_tab_with_anonymous_user(self):
		'''
		ValueError must be raised when anonymous user tries to create new tab
		'''
		self.assertRaises(ValueError, Tab.objects.create_tab, user=None, name='Hello')

	'''
	-------------------------
	TabSource tests
	-------------------------
	'''
	def test_add_source(self):
		'''
		add_source must associate the source with the tab. If the tab is none, no error must be displayed.
		The new source must automatically be assigned the last priority
		'''
		#Adding an existing source returns None
		self.assertIsNone(self.tab.add_source(source=self.source))

		#A new source should automatically have the lowest priority (highest number)
		source = Source.objects.create(name='Hindu', link='http://hindu.com')
		self.tab.add_source(source)
		tabsource = get_object_or_none(TabSource, tab=self.tab, source=source)
		self.assertEqual(tabsource.source_priority, self.tabsource.source_priority + 1)
		
		#Adding an empty source should not raise an exception
		self.assertIsNone(self.tab.add_source(None))

	def test_get_sources(self):
		'''
		get_sources must return the list of sources in the tab if present, empty list otherwise
		'''
		#If the tab has sources, the respective sources must be returned
		sources = self.tab.get_sources()
		self.assertEqual(len(sources), 1)
		self.assertTrue(sources[0], self.source)

		#If no sources are available, empty list must be returned
		new_tab = Tab.objects.create_tab(user=self.user, name='Random')
		sources = new_tab.get_sources()
		self.assertFalse(sources)

	def test_delete_source(self):
		'''
		delete_source must delete the source associated with this tab. If the source is not associated with this tab, no error must be provided
		'''
		#If the source is None, it should not give any error
		self.assertIsNone(self.tab.delete_source(None))

		#If the source is not associated with the tab, None should be returned
		source = Source.objects.create(name='Hello, world', link='http://abc.com')
		self.assertIsNone(self.tab.delete_source(source))

		#The source object is returned if the deletion was successful
		self.assertEqual(self.tab.delete_source(self.source), self.source)

	def test_change_source_priority(self):
		'''
		change_source_priority must change the priority of the source to the specified priority
		'''
		#No error must be raised when source is none
		self.assertIsNone(self.tab.change_source_priority(None, 2))

		#Invalid priority must not result in any change
		self.assertEqual(self.tab.change_source_priority(self.source, 0), self.tabsource.source_priority)
		self.assertEqual(self.tab.change_source_priority(self.source, 100), self.tabsource.source_priority)

		#When a valid priority is set, its priority must be changed accordingly and the priority of the rest of the sources must be reordered
		new_source = Source.objects.create(name='My Source', link='http://abcd.com')
		self.tab.add_source(new_source)
		self.assertEqual(self.tab.change_source_priority(self.source, 2), 2)
		self.assertEqual(self.tab.get_sources(), [new_source, self.source])