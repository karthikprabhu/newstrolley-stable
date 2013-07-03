from datetime import datetime, date
from dateutil.tz import tzlocal
from dateutil.relativedelta import relativedelta

import logging
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