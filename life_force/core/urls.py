from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('client_signup/', views.Client_sign_up, name='signup'),
    path('Organisation_signup/', views.Organization_sign_up),
    path('gett', views.get_token),
    path('login_user', views.login_user),
    path('complete_client_registration/', views.complete_client_registration),
    path('complete_organization_registartion', views.complete_orgaanization_registration),
    path('kyc/', views.kyc_verification),
    path('dashboard', views.dashboard),
    path('marketplace', views.marketpalce)

]