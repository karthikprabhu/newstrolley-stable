from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from models import Feedback

import logging
logger = logging.getLogger(__name__)

@dajaxice_register
def post_feedback(request, subject, text):
	logger.debug("Ajax request received for feedback.")
	success = False
	
	if request.user.is_authenticated():
		user = request.user
		logger.info("Submitting feedback for "+str(user))
		
		fb = Feedback()
		fb.user = user
		fb.subject = subject
		fb.text = text
		fb.save()
		
		success = True
	
	return simplejson.dumps({'success':success})
