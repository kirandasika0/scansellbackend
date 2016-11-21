from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^new_sale/', views.new_sale),
    url(r'^title_case_string/', views.title_case_string),
    url(r'^new_sale_interest/', views.new_sale_interest),
    url(r'^new_sale_insert/', views.new_sale_insert),
    url(r'^redis_test/', views.redis_test),
    url(r'^create_locale/', views.create_locale),
    url(r'^get_feed/', views.get_feed),
    url(r'^sale_notification/', views.sale_notification),
    url(r'^get_notifications/', views.get_notifications),
    url(r'^delete_notification/', views.delete_notification),
    url(r'^test_patch/', views.test_patch),
    url(r'^geo_feed/', views.geo_feed_view),
    url(r'geo_feedv2/', views.geo_feedv2),
    url(r'slider_feed/', views.sliderFeed),
    url(r'hot_deals/', views.hotDeals),
    url(r'sale_images/',views.getSaleImages),
    url(r'place_bid/', views.placeBid),
]
