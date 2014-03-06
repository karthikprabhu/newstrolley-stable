from django.core.management import setup_environ
from newstrolley import settings

setup_environ(settings)

from newsreader import models
import csv

import logging
logger = logging.getLogger(__name__)

reader = csv.reader(open('feeds.txt'), delimiter=',')
for row in reader:
    s = models.Source(link=row[0], name=row[1])
    try:
        s.save()
    except:
        logger.debug("Could not save source: "+str(s))

    print 'added:', s.name
