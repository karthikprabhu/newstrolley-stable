from newsreader.models import Tab
from accounts.models import NTUser
from taggit.models import Tag

import urllib
import json

import logging
logger = logging.getLogger(__name__)

'''
---------------------------
Tag retreival for articles
---------------------------
'''
def get_tags(url):
	tags = []

	try:
		query_url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20contentanalysis.analyze%20where%20url%3D'"+url+"'%3B&format=json&diagnostics=true&callback=cbfunc"
		content = urllib.urlopen(query_url).read()

		result = json.loads(content[7:len(content)-2])
		results = result.get('query', {}).get('results')

		if results:
			categories = results.get('yctCategories', {}).get('yctCategory')
			if categories:
				for category in categories:
					if isinstance(category, dict):
						tags.append(category.get('content'))

			entities = results.get('entities', {}).get('entity')
			if entities:
				for entity in entities:
					if isinstance(entity, dict):
						tags.append(entity.get('text', {}).get('content'))
	except Exception,e:
		logger.exception(e)

	return list(set(tags))