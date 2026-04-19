from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('voitures/', views.admin_cars, name='admin_cars'),
    path('voitures/ajouter/', views.admin_car_add, name='admin_car_add'),
    path('voitures/<int:pk>/modifier/', views.admin_car_edit, name='admin_car_edit'),
    path('voitures/<int:pk>/supprimer/', views.admin_car_delete, name='admin_car_delete'),
    path('reservations/', views.admin_bookings, name='admin_bookings'),
    path('reservations/<int:pk>/statut/', views.admin_booking_update, name='admin_booking_update'),
]
