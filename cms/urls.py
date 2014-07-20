from django.conf.urls import patterns, include, url

urlpatterns = patterns('cms.views',
	url(r'm/home', 'mobilehome', name='cms_mobile_home'),
	url(r'm/(?P<name>[a-zA-Z0-9-]+)/?', 'mobile', name='cms_mobile'),
	url(r'(?P<name>[a-zA-Z0-9-]+)/?', 'main', name='cms'),
)
