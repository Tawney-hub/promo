from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('scan/<slug:slug>/', views.scan_landing, name='scan_landing'),
    path('claim/', views.claim_reward, name='claim_reward'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-media/', views.update_media_content, name='update_media_content'),
    path('upload-music/', views.upload_music, name='upload_music'),
    path('create-location/', views.create_location, name='create_location'),
    path('create-promo/', views.create_promo, name='create_promo'),
    path('export-leads/', views.export_leads_csv, name='export_leads_csv'),
]
