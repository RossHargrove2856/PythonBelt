from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^createItem$', views.createItem),
    url(r'^addItem$', views.addItem),
    url(r'^item/info/(?P<item_id>\d+)$', views.itemInfo),
    url(r'^addWishlist/(?P<item_id>\d+)$', views.addWishlist),
    url(r'^removeWishlist/(?P<item_id>\d+)$', views.removeWishlist),
    url(r'^destroy/(?P<item_id>\d+)$', views.destroy),
]