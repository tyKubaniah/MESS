from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'), # Handled cleanly now!
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('toggle/<int:item_id>/', views.toggle_menu_item, name='toggle_menu_item'),
]