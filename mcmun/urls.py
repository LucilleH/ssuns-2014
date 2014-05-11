from django.conf.urls import patterns, include, url
from mcmun.pages import pages
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# for development use
from django.conf import settings
#from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'cms.views.main', name='home'),
    url(r'^dashboard', 'mcmun.views.dashboard', name='dashboard'),
    url(r'^assignments', 'mcmun.views.assignments', name='assignments'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^committees/', include('committees.urls')),
#    url(r'^staff-application/', include('staffapps.urls')),
#    url(r'^signups/', include('signups.urls')),
    url(r'^registration-tmp', 'mcmun.views.registration', name='registration'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^password$', 'django.contrib.auth.views.password_change', {'template_name': 'password.html', 'post_change_redirect': '/password_success'}, name='password'),
    url(r'^password_success$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_success.html'}, name="password_success"),

    url(r'^password_reset$', 'django.contrib.auth.views.password_reset', {'template_name': 'password_reset.html', 'from_email': settings.IT_EMAIL, 'email_template_name': 'password_reset_email.html', 'subject_template_name': 'password_reset_subject.txt'}, name="password_reset"),
    url(r'^password_reset_done$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'password_reset_done.html'}, name="password_reset_done"),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html', 'post_reset_redirect' : '/password_reset_complete'}, name="password_reset_confirm"),
    url(r'^password_reset_complete$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_complete.html'}, name="password_reset_complete"),
    url(r'^position-papers/(?P<file_name>[^/]+)', 'committees.views.serve_papers'),
    url(r'^scholarship/individual/(?P<file_name>[^/]+)', 'committees.views.serve_scholarship'),
    url(r'^scholarship/school/(?P<file_name>[^/]+)', 'mcmun.views.serve_scholarshipschool'),
    url(r'^scholarship_list$', 'committees.views.list_scholarship', name='list_scholarship'),
#    url(r'^delegatesurvey', 'mcmun.views.delegate_survey', name='delegate_survey'),
#    url(r'^surveyresult', 'mcmun.views.survey_result', name='survey_result'),
    url(r'^nikhilerror$', 'mcmun.views.nikhil_error'),
    url(r'^', include('cms.urls')),
)
