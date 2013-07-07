from django.core.management import setup_environ
from newstrolley import settings as nt_settings

setup_environ(nt_settings)

from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.simple import DjangoTestSuiteRunner

import os
import sys

def test_app(app_name, runner):
	print "Testing app '%s'" % str(app_name)
	if runner.run_tests([app_name]) == 0:
		print "Test successful"
	else:
		print "Error in app '%s'. Rectify the errors and start again" % str(app_name)
		exit(1)

def main():
	setup_test_environment()
	runner = DjangoTestSuiteRunner()
	
	app_order = ["accounts", "newsreader", "tags"]
	for app in app_order:
		test_app(app, runner)

	response = raw_input("Testing 'feeds' app will take a while. Would you like to continue? (yes/no): ")
	if response == "yes":
		test_app(app, runner)

	# teardown_test_environment()
	path = os.getcwd() + "/newsreader/static/newsreader/media/tab_thumbs/small_image.jpg"
	if os.path.isfile(path):
		os.remove(path)

	exit(0)
main()