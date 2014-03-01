from django.conf.urls import patterns, include, url

#urlpatterns = patterns('signups.views',
#	url(r'^(?P<category>\w+)/?$', 'submit', name='submit_signup'),
#)
urlpatterns = patterns('signups.views',
	url(r'^$', 'submit', name='submit_signup'),
)
