from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update/<int:post_id>/<str:action>", views.update_post, name='update_post'),
    path("new", views.new_post, name='new_post'),
]