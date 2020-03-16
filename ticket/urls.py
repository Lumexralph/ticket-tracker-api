from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ticket import views

urlpatterns = [
    path('', views.ListTicket.as_view()),
    path('', views.CreateTicket.as_view()),
    path('<int:ticket_id>/assign/<int:admin_id>', views.AssignTicketToAdmin.as_view()),
    path('<int:ticket_id>/reject', views.RejectTicket.as_view()),
    path('<int:ticket_id>/accept', views.AcceptTicket.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
