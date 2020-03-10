from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
    path('signup', views.UserRegistration.as_view(), name='account-registration'),
    path('login', views.UserLogin.as_view(), name='user-login'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='retrieve-user'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
