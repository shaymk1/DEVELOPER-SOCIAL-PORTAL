"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path
from  . import views


urlpatterns = [

    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    
    path('', views.profiles, name = "profiles"),
    # path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('user_profile/<str:pk>/', views.user_profile, name="user_profile"),
    path('account/', views.user_account, name ='account'),
    path('edit_account/', views.edit_account, name="edit_account"),

    
    path('create_skill/', views.create_skill, name="create_skill"),
    path('update_skill/<str:pk>/', views.update_skill, name="update_skill"),
    path('delete_skill/<str:pk>/', views.delete_skill, name="delete_skill"),

    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.view_message, name="message"),
    path('create_message/<str:pk>/', views.create_message, name="create_message"),
  

]
    

