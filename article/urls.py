from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'news/(?P<news_id>\w+?)/$', views.news_detail_view, name='news-detail'),
]
