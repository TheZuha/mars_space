from django.urls import path

from shop.views import shop_view, detail_product, buy_product, shop_history_view

urlpatterns = [
    path('', shop_view, name='shop'),
    path('products/<int:id>/', detail_product, name='detail_product'),
    path('products/<int:id>/buy/', buy_product, name='buy_product'),
    path('history/', shop_history_view, name='shophistory'),
]
