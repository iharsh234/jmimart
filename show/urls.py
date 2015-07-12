from django.conf.urls import url, patterns
from show import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^item/(?P<id>[0-9]+)', views.item, name='item'),
    url(r'^books/$', views.books, name='books'),
    url(r'^stationary/$', views.stationary, name='stationary'),
    url(r'^others/$', views.others, name='others'),
)
