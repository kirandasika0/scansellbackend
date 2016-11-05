from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home), 
    url(r'^insert_book/', views.insert_book),
    url(r'^new_search/', views.new_search),
    url(r'^search_book/', views.search_book),
    url(r'star_book/(?P<id>[0-9]+)/$', views.star_book),
    url(r'book_details/', views.bookDetails),
]