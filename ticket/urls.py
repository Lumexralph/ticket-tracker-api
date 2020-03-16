from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ticket import views

urlpatterns = [
    path('', views.ListTicket.as_view()),
    path('', views.CreateTicket.as_view()),
    path('<int:ticket_id>/assign/<int:admin_id>', views.AssignTicketToAdmin.as_view()),
    # path('<int:pk>/book/', views.BookTicket.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)