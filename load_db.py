from django.core.management import setup_environ
from newstrolley import settings

setup_environ(settings)

from newsreader import models
import csv

reader = csv.reader(open('feeds.txt'), delimiter=',')
for row in reader:
    s = models.Source(link=row[0], name=row[1])
    s.save()

    print 'added:', s.name