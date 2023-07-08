from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.base, name="base"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('usernamevalidate',csrf_exempt(views.usernamevalidate), name="usernamevalidate"),
    path('emailvalidate', csrf_exempt(views.emailvalidate), name="emailvalidate"),
    path('activate/<uidb64>/<token>/', views.verify, name = 'activate'),
]