from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
    path('signup', views.UserRegistration.as_view(), name='account-registration'),
    path('login', views.UserLogin.as_view(), name='user-login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
