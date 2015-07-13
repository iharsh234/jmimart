from django.conf.urls import url, patterns
from show import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^item/(?P<id>[0-9]+)', views.item, name='item'),
    url(r'^books/(?P<p>[0-9]*)', views.books, name='books'),
    url(r'^stationary/(?P<p>[0-9]*)', views.stationary, name='stationary'),
    url(r'^others/(?P<p>[0-9]*)', views.others, name='others'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^tnc/$', views.tnc, name='tnc'),
)
