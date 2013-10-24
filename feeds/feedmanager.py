from django.core.cache import cache

from feeds.models import Article
from taggit.models import Tag

import feedparser as fp

from dateutil import parser as date
from dateutil.tz import tzlocal
from dateutil.relativedelta import relativedelta as timedelta
from datetime import datetime, timedelta as delta

from newstrolley.utils import get_object_or_none, format_datetime
from newsreader.models import Source, Tab

import logging
logger = logging.getLogger(__name__)

CACHE_EXPIRES = 5 * 60 # 5 minutes
UPDATE_INTERVAL = 2 #in hours

def update_feed(source):
	'''
	Updates the feeds from source if it has not been updated for UPDATE_INTERVAL hours
	'''
	logger.info("Checking if %s needs to be updated" % str(source))
	#Get the last update time
	if source:
		last_update = source.last_update
	updated_articles = []
	logger.debug("%s was last updated: %s" % (str(source), format_datetime(last_update)))

	#Update only if UPDATE_INTERVAL time has elapse since the last update
	if not last_update or timedelta(datetime.now(tzlocal()), last_update) >= timedelta(hours=UPDATE_INTERVAL):
		logger.info("Updating source %s" % str(source))
		feed = fp.parse(source.link)
		
		for entry in feed.get('entries'):
			#Try parsing the date and if it thows an exception, default to the current date
			try:
				pub_date = date.parse(entry.get('published'), default=datetime.now(tzlocal()))
			except:
				pub_date = datetime.now(tzlocal())

			link = entry.get('link')
			heading = entry.get('title')
			summary = entry.get('summary_detail').get('value')
			logger.debug("Parsed article: %s" % u''.join(heading).encode('utf-8').strip())

			#Check if article has already been added.
			article = get_object_or_none(Article, link=link)
			if not article:
				try:
					logger.debug("Article not found in database. Adding to database")
					article = Article.objects.create(pub_date=pub_date, link=link, source=source, heading=heading, summary=summary)
					article.tag_self()
					updated_articles.append(article)
				except Exception, e:
					logger.exception(e)

		#Update the last update time of this source
		source.last_update = datetime.now(tzlocal())
		source.save()
		logger.info("No of articles updated: %d" % len(updated_articles))

	return updated_articles

def get_content(user, tab_id):
	'''
	Returns a list of articles. Loads from cache if available.
	'''
	logger.info("Retrieving content for tab_id %s" % int(tab_id))
	
	#Try finding articles in cache
	cache_key = "tab_cache" + str(user.id) + str(tab_id)
	articles = cache.get(cache_key, [])
	logger.debug("No of articles found in cache: %d (cache_key=%s)" % (len(articles), cache_key))
	
	#If the articles are not found in the cache, then retreive the articles
	if not articles:
		logger.info("Trying to retrieve articles from database")
		tab = get_object_or_none(Tab, id=tab_id, user=user)
		
		articles = []
		tagged_articles = []
		
		if tab is not None:
			logger.debug("Tab found: %s. Getting sources and tags" % str(tab))
			#Get all the sources and tags in the tab
			sources = tab.get_sources() #This makes sure that the articles are arranged in order of source priority
			tags = tab.tags.all()
			logger.debug("Sources: %s, Tags: %s" % (str(sources), str(tags)))

			#For each source, retrieve the articles
			for source in sources:
				logger.debug("Retrieving articles for source: %s" % str(source))
				
				#Make sure the source has the latest feeds
				update_feed(source)
				source_articles = Article.objects.filter(source=source, pub_date__gt=datetime.now(tzlocal())-delta(days=1)).order_by('-pub_date')
				logger.debug("No of source articles found: %d" % len(source_articles))

				#If tags are specified, filter articles with tags
				if tags:
					logger.debug("Filtering articles based on the tags")
					tagged_articles_in_source = source_articles.filter(tags__in=tags).distinct()
					
					tagged_articles += tagged_articles_in_source
					# source_articles -= tagged_articles_in_source
					temp_articles = []
					temp_articles += source_articles
					for t_article in tagged_articles_in_source:
						temp_articles.remove(t_article)
					
					logger.debug("No of tagged articles: %s" % len(tagged_articles))

					articles += temp_articles
				else:
					articles += source_articles
			
			articles = tagged_articles+articles
			
			logger.info("No of articles retrieved: %d" % len(articles))
			logger.info("Adding articles to cache")
			
			#add the articles to cache
			cache.add(cache_key, articles, CACHE_EXPIRES)

	return articles