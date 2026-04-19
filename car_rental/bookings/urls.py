from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:car_pk>/', views.book_car, name='book_car'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    path('mes-reservations/', views.my_bookings, name='my_bookings'),
    path('annuler/<int:pk>/', views.cancel_booking, name='cancel_booking'),
]
