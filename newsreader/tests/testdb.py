from accounts.models import NTUser
from newsreader.models import Source, Tab, TabSource

from django.core.urlresolvers import reverse

'''
-------------------------
Setup test database
-------------------------
'''
def setup_db(obj):
	#Make sure constants are setup
	obj.base_url = 'http://testserver'
	obj.landing_page_url = obj.base_url + reverse('newsreader:index')
	obj.login_error_url = obj.landing_page_url + '?login_error=1'
	obj.home_page_url = obj.base_url + reverse('newsreader:home')

	obj.user_name = 'Karthik'
	obj.user_email = 'k.karthik.prabhu@gmail.com'
	obj.user_pass = 'Dazedanddoped1'
	
	#Setup sources
	obj.sources = [
		Source.objects.create(name='CNN-IBN Top Stories', link='http://www.ibnlive.com/xml/top.xml'),
		Source.objects.create(name='Hindu: Home', link='http://www.thehindu.com/?service=rss'),
		Source.objects.create(name='Hindustan Times: Top Stories', link='http://feeds.hindustantimes.com/HT-HomePage-TopStories'),
		Source.objects.create(name='Times Now: National', link='http://www.timesnow.tv/Rssfeeds/India.Xml'),
		Source.objects.create(name='Indian Express: Latest', link='http://www.indianexpress.com/rss/latest-news.xml'),
	]

	#Create user. Default tab will automatically be created
	obj.user = NTUser.objects.create_user(name=obj.user_name, email=obj.user_email, password=obj.user_pass)

	obj.tabs = [
		Tab.objects.get(user=obj.user, name='Headlines'), #Get the default tab
		Tab.objects.create_tab(user=obj.user, name='National'),
		Tab.objects.create_tab(user=obj.user, name='Local'),
	]
	obj.tabs.sort(key=lambda tab: tab.order)#sort in ascending order of order numbers

	#Add sources to tabs
	obj.tabs[0].add_source(obj.sources[1])
	obj.tabs[0].add_source(obj.sources[2])

	obj.tabs[1].add_source(obj.sources[0])
	obj.tabs[1].add_source(obj.sources[1])