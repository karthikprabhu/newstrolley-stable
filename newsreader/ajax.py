from django.utils import simplejson
from django.core import cache
from django.contrib.auth.models import AnonymousUser

from dajaxice.decorators import dajaxice_register

from newsreader.models import Tab, Source, TabSource
from newstrolley.utils import get_object_or_none

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