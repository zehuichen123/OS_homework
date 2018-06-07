from django.conf.urls import url

from . import views

app_name='simulator'
urlpatterns=[
	url(r'index/$',views.index,name='index'),
	url(r'lru/$',views.lru,name='lru'),
	url(r'fifo/$',views.fifo,name='fifo'),
	url(r'readme/$',views.readme,name='readme'),
]