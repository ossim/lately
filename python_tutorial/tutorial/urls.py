from django.conf.urls import patterns, url
from tutorial import views

urlpatterns = patterns('',
    # The home view ('/tutorial/')
    url(r'^$', views.home, name='home'),
    # Explicit home ('/tutorial/home/')
    url(r'^home/$', views.home, name='home'),
    # Redirect to get token ('/tutorial/gettoken/')
    url(r'^gettoken/$', views.gettoken, name='gettoken'),
    # Rojw
    url(r'^post/form_upload.html$', views.post_form_upload, name='post_form_upload'),
    # Send view ('/tutorial/send/')>
    url(r'^send/$', views.send, name='send'),
    # Success view
    url(r'^success/$', views.success, name='success'),
)
