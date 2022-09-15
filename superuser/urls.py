from django.urls import path

from superuser import admin
from . import views




urlpatterns = [
    path('' , views.admin_home , name="admin-home"), 
    path('add-product/' , views.admin_product , name="admin-add-product"),
    path('delete-product/<str:id>/' , views.admin_product_delete , name="admin-delete-product"),
    path('update-product/<str:id>/',views.admin_product_update , name="admin-update-product"),
    path('admin-login/' , views.admin_login , name="admin-login"),
    path('admin-logout/' , views.admin_logout , name="admin-logout"),
    path('admin-user-list/' , views.admin_user_list , name="admin-user-list"),
    path('admin-user-block/<str:id>/' ,  views.admin_user_block , name="admin-user-block"),
    path('admin-category/' , views.admin_category , name="admin-category"),
    path('update-category/<str:id>/',views.admin_category_update , name="admin-update-category"),
    path('delete-category/<str:id>/' , views.admin_category_delete , name="admin-delete-category"),
    path('add-category/' , views.admin_category_add , name="admin-add-category"),
    path('product-list/' , views.admin_product_list , name="admin-product-list"),
    path('order-list/' , views.admin_order , name="admin-order"),
    path('update-status/<str:id>/' , views.admin_update_status , name="order-status"),
    path('offer/' , views.offer , name="admin-offer"),
    path('delete-offer/<str:id>/' , views.offer_delete , name="admin-delete-offer"),
    path('add-offer/' , views.offer_add , name="admin-add-offer"),
    path('update-offer/<str:id>/',views.offer_update , name="admin-update-offer"),
]
