from django.utils import simplejson
from django.core.cache import cache

from dajaxice.decorators import dajaxice_register

from tags.models import Rule
from taggit.models import Tag

from newsreader.models import Tab
from newstrolley.utils import get_object_or_none

@dajaxice_register
def add_tag(request, tab_id, tag):
	success = False
	
	tab = get_object_or_none(Tab, id=tab_id, user=request.user)
	if tab:
		tab.add_tag(tag)
		tab.save()
		success = True

	return simplejson.dumps({ "success": success })

@dajaxice_register
def delete_tag(request, tab_id, tag):
	success = False
	
	tab = get_object_or_none(Tab, id=tab_id, user=request.user)
	if tab:
		tab.delete_tag(tag)
		tab.save()
		success = True

	return simplejson.dumps({ "success": success })

@dajaxice_register(method='GET')
def get_tags(request, query):
	tag_names = []
	if query:
		tags = Tag.objects.filter(name__contains=query)
		tag_names = [tag.name for tag in tags]
	
	return simplejson.dumps({ "tags": tag_names })

@dajaxice_register(method='GET')
def get_tab_tags(request, tab_id):
	tab = get_object_or_none(Tab, id=tab_id, user=request.user)
	tags = []
	if tab:
		tags = [tag.name for tag in tab.tags.all()]
	
	return simplejson.dumps({ "tags": tags })