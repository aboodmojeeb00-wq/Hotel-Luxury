from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Renamed home to landing and moved off root to allow Login to be root
    path('welcome/', views.home, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/add/', views.room_create, name='room_create'),
    path('rooms/<int:pk>/edit/', views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', views.room_delete, name='room_delete'),

    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/add/', views.booking_create, name='booking_create'),
    path('bookings/<int:pk>/edit/', views.booking_update, name='booking_update'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),

    path('payments/', views.payment_list, name='payment_list'),

    path('reviews/', views.review_list, name='review_list'),
    path('reviews/add/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/edit/', views.review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
