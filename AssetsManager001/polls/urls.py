from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    # ホーム
    path('', views.MainView.as_view(), name='main'),
    # 貸出情報一覧
    path('lend/', views.lend, name='lend'),
    path('lend/sort/<int:column_number>/', views.lendSort, name='lendSort'),
    path('lend/delete/', views.lendDelete, name='lendDelete'),
    # 機器一覧
    path('devices/', views.devices, name='devices'),
    path('devices/sort/<int:column_number>/', views.devicesSort, name='devicesSort'),
    path('devices/delete/', views.devicesDelete, name='devicesDelete'),
    # 社員一覧
    path('users/', views.users, name='users'),
    path('users/sort/<int:column_number>/', views.usersSort, name='usersSort'),
    path('users/delete/', views.usersDelete, name='usersDelete'),
    # 貸出情報管理
    path('lend/add/', views.lendAdd, name='lendAdd'),
    path('lend/edit/<int:pk>/', views.lendEdit, name='lendEdit'),
    # 機器情報入力
    path('devices/edit/<int:pk>/', views.devicesEdit, name='devicesEdit'),
    # 社員情報入力
    path('users/edit/<int:pk>/', views.usersEdit, name='usersEdit'),
]