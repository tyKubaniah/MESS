from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('toggle-item/<int:item_id>/', views.toggle_menu_item, name='toggle_menu_item'),
]