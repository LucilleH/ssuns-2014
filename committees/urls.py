from django.conf.urls import patterns, include, url

SLUG = r'^(?P<slug>[a-zA-Z0-9-]+)'

urlpatterns = patterns('',
    # Redirect committees/ back to committees (show the page)
    url(r'^$', 'cms.views.main', name='committees'),
    url(SLUG + '/manage$', 'committees.views.manage', name='committee_manage'),
    url(SLUG + '/awards$', 'committees.views.awards', name='committee_awards'),
    url(r'^(?P<slug>[a-zA-Z0-9-]+)/papers$', 'committees.views.list_papers', name='list_papers'),
    url(r'^m/(?P<slug>[a-zA-Z0-9-]+)', 'committees.views.view_mobile', name='committee_view_mobile'),
    url(SLUG, 'committees.views.view', name='committee_view'),
)
