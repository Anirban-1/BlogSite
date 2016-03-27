from django.conf.urls import url
from blog_app import views

#mystring = '^home/$'
urlpatterns = [
    url(r'^$', views.face, name = 'face'),  # show the home page
    url(r'^registration/$', views.init_register, name = 'initRegister'), # call the page to initiate registration
    url(r'^register/$', views.register, name='register'), # register the user
    url(r'^initlogin/$', views.init_login, name='initLogin'), # call the page to initiate login
    url(r'^login/$', views.login, name='login'), #log in the user
    url(r'^logout/$', views.logout_view, name='logout'), # log out user
    url( r'^home/(?P<user>[a-z,A-Z]+)/$', views.home, name='home'),  #r'^home/$
    url(r'^publish_post/$', views.publish, name='publish'),
    url(r'^post/(?P<user>[a-z,A-Z]+)/(?P<post_id>[0-9]+)/$', views.post_details, name='post_details'),
    url(r'^post/all/(?P<user>[a-z,A-Z]+)/$', views.all_posts, name='all_posts'),
    url(r'^home/(?P<user>[a-z,A-Z]+)/follow/$', views.follow, name='follow'),
    url(r'^(?P<user>[a-z,A-Z]+)/following/$', views.follow_list_view, name='follow_list'),
]
