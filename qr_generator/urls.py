from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_qr, name='generate_qr'),
    path('download_qr/', views.download_qr, name='download_qr'),  # URL para descargar el QR
]
