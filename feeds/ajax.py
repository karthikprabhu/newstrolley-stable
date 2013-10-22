from django.core.cache import cache

from django.utils import simplejson
from django.core.urlresolvers import reverse

from dajaxice.decorators import dajaxice_register

from feeds.feedmanager import get_content
from newstrolley.utils import format_datetime, generate_seo_link

from models import Article

import logging
logger = logging.getLogger(__name__)

ARTICLE_TIMEOUT = 60 * 60 # 60 minutes = 1 hr

@dajaxice_register(method='GET')
def article_viewed(request, article_id):
	cache_key = str(article_id)
	article_count = cache.get(cache_key, 0)+1
	
	cache.set(cache_key, article_count, ARTICLE_TIMEOUT)
	
	top_ten = cache.get("top_ten", {})
	in_cache = article_id in top_ten
	if not in_cache:
		if len(top_ten)<10:
			top_ten[article_id] = article_count
		else:
			min=-1
			min_key=0
			for key, value in top_ten:
				if value<=min:
					min = value
					min_key = key
			
			top_ten.pop(min_key)
			
			top_ten[article_id] = article_count
		
		cache.set("top_ten", top_ten, None)
	
	return {"in_top_ten":in_cache}


@dajaxice_register(method='GET')
def get_top_ten(request):
	top_ten = cache.get("top_ten", {})
	top_ten_articles = []
	response = {"top_ten":top_ten_articles}
	for article_id in top_ten:
		article = Article.objects.get(id=article_id)
		top_ten_articles.append({"heading":article.heading,
		                            "link":reverse('newsreader:article', kwargs={'article_url': generate_seo_link(article.get_heading()), 
							  "article_id": article.id})
								})
	
	return response

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
				'id': article.id,
				'title': article.get_heading(),
				'mlink': article.link,
				'link': reverse('newsreader:article', kwargs={'article_url': generate_seo_link(article.get_heading()), 'article_no': article.id}), 
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