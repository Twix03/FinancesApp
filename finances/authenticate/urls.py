from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('usernamevalidate',csrf_exempt(views.usernamevalidate), name="usernamevalidate"),
    path('emailvalidate', csrf_exempt(views.emailvalidate), name="emailvalidate"),
    path('activate/<uidb64>/<token>/', views.verify, name = 'activate'),
    path('signout', views.signout, name='signout'),
    path('resetpassword/', views.reset_password, name="reset_password"),
    path('reset/newpassword/<uidb64>/<token>/', views.new_password, name="new_password")
]