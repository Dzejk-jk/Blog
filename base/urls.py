from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post/<str:pk>/', views.post, name='post'),

    path('create-post/', views.create_post, name='create-post'),
    path('update-post/<str:pk>/', views.update_post, name='update-post'),
    path('delete-post/<str:pk>/', views.delete_post, name='delete-post'),
    path('delete-comment/<str:pk>/', views.delete_comment, name="delete-comment"),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),

    path('search/', views.search_view, name='search'),
]