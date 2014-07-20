from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Redirect committees/ back to committees (show the page)
    url(r'^$', 'cms.views.main', name='committees'),
    url(r'^(?P<slug>[a-zA-Z0-9-]+)/papers$', 'committees.views.list_papers', name='list_papers'),
    url(r'^m/(?P<slug>[a-zA-Z0-9-]+)', 'committees.views.view_mobile', name='committee_view_mobile'),
    url(r'^(?P<slug>[a-zA-Z0-9-]+)', 'committees.views.view', name='committee_view'),
)
