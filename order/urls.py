from django.urls import path,include

from . import views


urlpatterns = [
   path('' ,views.place_order , name="place-order"),
   path('payments/' ,views.payments , name="payments"),
   path('order-complete/' ,views.order_complete , name="order-complete"),
   path('order-list/' ,views.order_list , name="order-list"),
   path('order-cancel/<str:id>' ,views.order_delete , name="order-cancel"),


] 
