from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('admin-panel/', views.AdminPanelView.as_view(), name='admin_panel'),
]
