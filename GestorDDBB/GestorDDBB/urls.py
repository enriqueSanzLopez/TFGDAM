"""
URL configuration for GestorDDBB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Gestor import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.login_view, name='inicio'),
    path('login/', views.login_controller, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main/', views.main_view, name='main'),
    path('users/', views.users_view, name='users'),
    path('users-edit/', views.create_user, name='users-edit'),
    path('users-password/', views.change_password, name='users-password'),
    path('users-delete/', views.delete_user, name='users-delete'),
    path('group/', views.group_view, name='group'),
    path('customize/', views.customize_view, name='customize'),
    path('customize-save/', views.customize_process, name='customize-save'),
]
