from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scan/<slug:slug>/', views.scan_landing, name='scan_landing'),
    path('claim/', views.claim_reward, name='claim_reward'),
]
