from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('article/<int:pk>/', views.ArticlePageView.as_view(), name = 'article_page'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name = 'archives'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name = 'category'),
    path('tag/<int:pk>/', views.TagView.as_view(), name = 'tag'),
    path('about/', views.about_page, name = 'about'),
    path('contact/', views.contact_page, name = 'contact'),
    # path('search/', views.search, name = 'search'),


]
