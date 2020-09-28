from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_pager, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update/<int:post_id>/<str:action>", views.update_post, name='update_post'),
    path("update/user/<int:user_id>/<str:action>", views.update_user, name='update_user'),
    path("new", views.new_post, name='new_post'),
    path('profile/<int:user_id>', views.profile_pager, name='profile'),
    path("following/<int:user_id>", views.following_pager, name='following'),
    path("followers/<int:user_id>", views.followers_pager, name='followers'),
    path("comments/<int:post_id>", views.comments, name='comments'),
    path("comments/add/<int:post_id>", views.add_comment, name='add_comment'),
    path("comments/del/<int:post_id>/<int:comment_id>", views.delete_comment, name='delete_comment'),
]