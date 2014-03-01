from django.conf.urls import patterns, include, url

urlpatterns = patterns('cms.views',
	url(r'(?P<name>[a-zA-Z0-9-]+)/?', 'main', name='cms'),
)
