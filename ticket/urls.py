from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ticket import views

urlpatterns = [
    # path('', views.ListTickets.as_view()),
    path('', views.CreateTicket.as_view()),
    # path('<int:pk>/', views.TicketDetail.as_view()),
    # path('<int:pk>/book/', views.BookTicket.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)