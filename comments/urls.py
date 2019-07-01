from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'comments'

urlpatterns = [
    # path('comment/article/<int:article_id>/', views.article_comment, name = 'article_comment'),
    url(r'^comment/article/(?P<article_id>[0-9]+)/$', views.article_comment, name = 'article_comment'),

]