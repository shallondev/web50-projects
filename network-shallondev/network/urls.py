
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("view_profile/<str:poster>/", views.view_profile, name="view_profile"),
    path('view_profile/<str:poster>/<str:follow>/', views.view_profile, name='view_profile_follow'),
    path('following/<str:username>/', views.index, name='following'),
    path('update_post/', views.update_post, name="update_post"),
    path('update_like/', views.update_like, name="update_like"),
]
