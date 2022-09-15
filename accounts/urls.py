from django.urls import path 
from . import views


urlpatterns = [
   path('', views.user_home ,name="home_user" ),
   path('signup/', views.register_user, name="signup_user"),
   path('signup-phone/', views.register_user_phone, name="signup_user_phone"),
   path('login/', views.login_user, name="login"),
   path('login-phone/', views.login_user_phone, name="login-phone"),
   path('logout/', views.logout_user, name="logout_user"),
   path('activate/<uidb64>/<token>/',views.activate_user, name="activate"),
   path('forgot_password/' , views.forgot_password , name='forgot_password'),
   path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name="resetpassword_validate"),
   path('reset_password/' , views.resetpassword , name='resetpassword'),
   path('userotp/', views.userotp, name='user_otp'),
   path('my-address/',views.user_address,name='user_address'),
   path('change-password/',views.change_password,name='change-password'),

    
]