from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import ngo_dashboard, ngo_login


urlpatterns = [
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'), 
    path('login/', views.login_view, name='login'), 
    path('donate/', views.donate, name='donate'),  
    path('donation-history/', views.donation_history, name='donation_history'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),  
    path('ngo-home/', views.ngo_home, name='ngo_home'),
    path('ngo-login/', views.ngo_login, name='ngo_login'),
    path('ngo-register/', views.ngo_register, name='ngo_register'),
    path('ngo-dashboard/', views.ngo_dashboard, name='ngo_dashboard'),  
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])