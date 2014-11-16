from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^forum$', 'twitter.views.forum'),
    url(r'^forum/json$', 'twitter.views.forum_json'),
    url(r'^forum/approve$', 'twitter.views.forum_approve'),
)
