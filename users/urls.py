from django.conf.urls import url, patterns
from users import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^new/$', views.new, name='new'),
    url(r'^item/(?P<id>[0-9]+)', views.item, name='item'),
    url(r'^edit/(?P<id>[0-9]+)', views.edit, name='edit'),
    url(r'^delete/(?P<id>[0-9]+)', views.delete_item, name='delete'),
    url(r'^sold/(?P<id>[0-9]+)', views.sold, name='sold'),
    url(r'^save/$', views.save, name='save'),
    url(r'^view/$', views.view, name='view'),
)
