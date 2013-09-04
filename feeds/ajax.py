from django.utils import simplejson
from django.core.urlresolvers import reverse

from dajaxice.decorators import dajaxice_register

from feeds.feedmanager import get_content
from newstrolley.utils import format_datetime

import logging
logger = logging.getLogger(__name__)

@dajaxice_register(method='GET')
def get_article(request, tab_id, article_no):
	logger.debug("Ajax request received.(Tab_id: %s, Article_no: %s)" % (tab_id, article_no))
	article = None
	success = False
	
	if request.user.is_authenticated():
		logger.info("Retreiving articles")
		
		articles = get_content(request.user, tab_id)
		
		logger.info("No of articles retreived: %d" % len(articles))
		
		if articles and len(articles) >= article_no:
			article = articles[article_no - 1]
			success = True

			logger.info("Article no %s found : %s" % (article_no, article.get_heading()))

			article = {
				'title': article.get_heading(),
				'link': reverse('newsreader:article', kwargs={'article_no': article.id}), 
				'pubDate': format_datetime(article.pub_date), 
				'summary': article.get_summary(), 
				'tags':[tag.name for tag in article.tags.all()]
			}
		else:
			article = {
				'no_articles': True
			}
	
	logger.debug("Sending response(%s)" % str(article))
	response = {'success': success, 'article': article}
	
	return simplejson.dumps(response)