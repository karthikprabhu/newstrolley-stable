from django.utils import simplejson
from django.core import cache
from django.contrib.auth.models import AnonymousUser

from django.core.urlresolvers import reverse

from dajaxice.decorators import dajaxice_register

from newsreader.models import Tab, Source, TabSource
from newstrolley.utils import get_object_or_none, generate_seo_link
from newsreader import mail

import feeds.models as feed_models

from datetime import date, timedelta

import logging
logger = logging.getLogger(__name__)

'''
-------------------------
Sources
-------------------------
'''
@dajaxice_register(method='GET')
def find_sources(request, query):
	logger.info("find_sources ajax request received(query=%s)" % query)
	
	if query:
		sources = Source.objects.filter(name__icontains=query)
	else:
		sources = []
	source_names = [source.name for source in sources]
	
	logger.debug("Sources found: %s" % str(source_names))
	logger.info("Sending response(find_sources)")
	return simplejson.dumps({'names': source_names})

@dajaxice_register(method='GET')
def get_sources(request, tab_id):
	logger.info("get_sources ajax request received(tab_id=%s)" % str(tab_id))
	
	source_names = []
	tab = get_object_or_none(Tab, user=request.user, id=tab_id)
	if tab:
		source_names = [source.name for source in tab.get_sources()]
		logger.debug("Sources found: %s" % str(source_names))
	
	logger.info("Sending response(get_sources)")
	return simplejson.dumps({'sources': source_names})

@dajaxice_register
def add_source(request, tab_id, source_name):
	logger.info("add_source ajax request received(tab_id=%s, source_name=%s)" % (str(tab_id), str(source_name)))
	
	success = False
	tab = get_object_or_none(Tab, user=request.user, id=tab_id)
	if tab:
		source = get_object_or_none(Source, name=source_name)
		if source:
			logger.debug("Adding %s to tab(%s)" % (str(source), str(tab)))
			tab.add_source(source)
			success = True

	logger.info("Sending response(add_source)")
	return simplejson.dumps({'success': success})

@dajaxice_register
def remove_source(request, tab_id, source_name):
	logger.info("remove_source ajax request received(tab_id=%s, source_name=%s)" % (str(tab_id), str(source_name)))

	success = False
	tab = get_object_or_none(Tab, user=request.user, id=tab_id)
	if tab:
		source = get_object_or_none(Source, name=source_name)
		if source:
			if tab.delete_source(source):
				logger.debug("Removed %s from tab(%s)" % (str(source), str(tab)))
				success = True

	logger.info("Sending response(remove_source)")
	return simplejson.dumps({'success': success})

@dajaxice_register
def change_source_position(request, tab_id, source_name, position):
	logger.info("change_source_position ajax request received(tab_id=%s, source_name=%s, position=%s)" % (str(tab_id), str(source_name), str(position)))

	success = False
	tab = get_object_or_none(Tab, user=request.user, id=tab_id)
	if tab:
		source = get_object_or_none(Source, name=source_name)
		if source:
			new_position = tab.change_source_priority(source, position)
			if new_position == position:
				logger.debug("%s position changed to %s" % (str(source), str(position)))
				success = True

	logger.info("Sending response(change_source_position")
	return simplejson.dumps({'success': success})

'''
-------------------------
Tabs
-------------------------
'''
@dajaxice_register
def change_tab_position(request, tab_id, position):
	logger.info("change_tab_position ajax request received(tab_id=%s, position=%s)" % (str(tab_id), str(position)))
	
	success = False
	tab = get_object_or_none(Tab, user=request.user, id=tab_id)
	if tab:
		if tab.change_order(position) == position:
			logger.debug("%s position changed to %s" % (str(tab), str(position)))
			success = True

	logger.info("Sending response(change_tab_position)")
	return simplejson.dumps({'success': success})

@dajaxice_register
def delete_tab(request, tab_id):
	logger.info("delete_tab ajax request received(tab_id=%s)" % str(tab_id))
	
	success = False
	tab = get_object_or_none(Tab, user=request.user, id=tab_id)
	if tab:
		tabsources = TabSource.objects.filter(tab=tab)
		tabsources.delete()
		tab.delete()
		logger.debug("%s tab deleted" % str(tab))
		success = True

	logger.info("Sending response(delete_tab)")
	return simplejson.dumps({'success': success})

'''
-------------------------
Account management
-------------------------
'''
@dajaxice_register
def resend_confirmation_mail(request):
	logger.info("Re-sending verification mail for user %s" % str(request.user))
	success = False

	if request.user.is_authenticated():
		#If the user is authenticated, then resend the mail only if the account is not verified
		if not request.user.verified:
			logger.debug("%s account is inactive" % str(request.user))
			name = request.user.name;
			email = request.user.email;
			token = request.user.get_email_confirmation_token()

			logger.debug("Sending verification mail to user %s with token %s" % (str(request.user), str(token)))
			mail.send_confirmation_mail(str(name), str(email), str(token))
			success = True

	logger.info("Sending response(resend_confirmation_mail)")
	return simplejson.dumps({'success': success})

'''
-------------------------
Ticker
-------------------------
'''
'''
@dajaxice_register
def get_top_ten(request):
	top_ten = cache.get("top_ten", {})
	top_ten_articles = []
	for article_id in top_ten:
		article = Article.objects.get(id=article_id)
		if not article:
			return
		top_ten_articles.append({"heading":article.heading,
		                       "orig_link":str(article.link),
		                            "link":reverse('newsreader:article', kwargs={'article_url': generate_seo_link(article.get_heading()), 
																				 'article_no':article.id})
								})
	
	return top_ten_articles
'''

@dajaxice_register
def get_ticker_feed(request):
	logger.info("Re-fetching ticker feed.")
	
	top_ten = cache.cache.get("top_ten", {})
	top_ten_articles = []
	for article_id in top_ten:
		article = feed_models.Article.objects.get(id=article_id)
		if not article:
			return
		top_ten_articles.append((article.heading,
		                        reverse('newsreader:article', kwargs={'article_url': generate_seo_link(article.get_heading()), 'article_no':article.id}),
								str(article.link)
								))
	logger.info("Sending response(get_ticker_feed)")
	return simplejson.dumps({'articles': top_ten_articles})