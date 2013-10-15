from datetime import datetime, date
from dateutil.tz import tzlocal
from dateutil.relativedelta import relativedelta

import logging
import re
logger = logging.getLogger(__name__)

def get_object_or_none(model, **kwargs):
	try:
		return model.objects.get(**kwargs)
	except model.DoesNotExist:
		return None
	except Exception, e:
		logger.exception(e)

def format_datetime(datetime):
	pub_date = ""
	
	if datetime:
		if datetime.date().day == date.today().day:
			now = datetime.now(tzlocal())
			diff = relativedelta(now, datetime)
			if diff.hours:
				pub_date = str(diff.hours) + " hour(s) ago"
			elif diff.minutes:
				pub_date = str(diff.minutes) + " minute(s) ago"
			else:
				pub_date = "1 minute ago"
		else:
			pub_date = datetime.strftime("%d %b, %Y")
	else:
		pub_date = "Unavailable"
	
	return pub_date

def generate_seo_link(input):
	out = re.sub(r' +', ' ', re.sub(r'[^a-zA-Z0-9\s]', '', input.lower()))
	out.strip()
	outarray = out.split(' ')
	tempout = []
	words = ('a', 'and', 'the', 'an', 'it', 'is', 'with', 'can', 'of', 'not', 
			'to', 'this', 'that', 'if', 'why', 'what', 'when', 'where', 'who', 'in', 
			'at', 'from', 'for', 'their', 'there', 'dont', 'on', 'as', 'than', 'its',
			'cant', 'too', 'be', 'has', 'been', 'did', 'i', 'my', 'have', 'you', 'do', 
			'get', 'no', 'am')
	for word in outarray:
		if word not in words and word not in tempout:
			tempout += [word]
	return '-'.join(tempout)