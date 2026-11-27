from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('superadmin/', views.superadmin, name='superadmin'),
    path('superadmin/category/add/', views.add_category, name='add_category'),
    path('superadmin/category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('superadmin/request/<int:request_id>/accept/', views.accept_request, name='accept_request'),
    path('superadmin/request/<int:request_id>/complete/', views.complete_request, name='complete_request'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.user_logout, name='logout'),
    path('request/create/', views.create_request, name='create_request'),
    path('request/<int:request_id>/delete/', views.delete_request, name='delete_request'),
]
