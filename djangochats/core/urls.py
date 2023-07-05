
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('',views.frontpage,name='frontpage'),
    path('signup/',views.signup,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
    path('personalchat/', views.Personalchatroom,name='personalchat'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('personal/<str:username>/',views.personalroominside,name='personalroom'),
    
]
