from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='regist'),
    path('index/', views.index_view, name='index'),
    path('logout/', views.logout_view, name='logout'),
]
