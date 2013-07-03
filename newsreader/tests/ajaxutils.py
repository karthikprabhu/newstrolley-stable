import urllib
import json

DAJAXICE_BASE = '/dajaxice/'

def dajaxice_get(client, app, method, params):
	data = {'argv': json.dumps(params)}
	return client.get(DAJAXICE_BASE + app + '.' + method + '/?' + urllib.urlencode(data),
		content_type='application/x-www-form-urlencoded',
		HTTP_X_REQUESTED_WITH='XMLHttpRequest',
	)

def dajaxice_post(client, app, method, params):
	data = {'argv': json.dumps(params)}
	return client.post(DAJAXICE_BASE + app + '.' + method + '/',
		data=urllib.urlencode(data),
		content_type='application/x-www-form-urlencoded',
		HTTP_X_REQUESTED_WITH='XMLHttpRequest')