from django.conf.urls import url

from . import views

app_name='elevator'
urlpatterns=[
	url(r'^index/$',views.index,name='index'),
    url(r'^start/$',views.start,name='start'),
	url(r'^request_up/(?P<stair_num>[0-9]+)/$',views.request_up,name='request_up'),
    url(r'^request_down/(?P<stair_num>[0-9]+)/$',views.request_down,name='request_down'),
    url(r'^ask_for_destination/(?P<elevator_num>[0-9])/(?P<stair_num>[0-9]+)/$',\
                    views.ask_for_destination,name="ask_for_destination"),
]