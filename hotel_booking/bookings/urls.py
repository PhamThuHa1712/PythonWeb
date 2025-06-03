from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('booking/<str:booking_id>/', views.booking_detail, name='booking_detail'),
    path('payment/<str:booking_id>/', views.payment, name='payment'),
    path('process_payment/<str:booking_id>/', views.process_payment, name='process_payment'),
    path('booking_history/', views.booking_history, name='booking_history'),
    path('create_booking/<str:room_id>/', views.create_booking, name='create_booking'),
    path('cancel_booking/<str:booking_id>/', views.cancel_booking, name='cancel_booking'),
]