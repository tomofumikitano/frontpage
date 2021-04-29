from django.urls import path

from . import views

app_name = 'feeds'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.handle_login, name='login'),
    path('logout', views.handle_logout, name='logout'),
    path('manage', views.manage, name='manage'),
    path('create/', views.create, name='create'),
    path('edit/<uuid:pk>', views.edit, name='edit'),
    path('delete/<uuid:pk>', views.delete, name='delete'),
]
