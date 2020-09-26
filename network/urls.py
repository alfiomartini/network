from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update/<int:post_id>/<str:action>", views.update_post, name='update_post'),
    path("update/user/<int:user_id>/<str:action>", views.update_user, name='update_user'),
    path("new", views.new_post, name='new_post'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path("following/<int:user_id>", views.following, name='following'),
    path("comments/<int:post_id>", views.comments, name='comments'),
    path("comments/add/<int:post_id>", views.add_comment, name='add_comment'),
    path("comments/del/<int:post_id>/<int:comment_id>", views.delete_comment, name='delete_comment'),
    
]