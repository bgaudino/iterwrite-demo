from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:paper_id>", views.index, name="index"),
    path("<int:paper_id>-<str:view>-<int:user_id>", views.index, name="index"),
    path("<int:paper_id>-<str:view>", views.index, name="index"),
    path("upload", views.upload, name="upload"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("compose", views.compose, name="compose"),
    path("add_comment/<int:paper_id>", views.add_comment, name="add_comment"),
    path("create_community", views.create_community, name="create_community"),
    path("join_community", views.join_community, name="join_community"),
    path("logout_view", views.logout_view, name="logout"),
    path("community-<str:community_name>", views.community, name="community"),
    path("profile-<str:username>", views.profile, name="profile"),
    path("edit", views.edit, name="edit"),
    path("leave_community-<int:community_id>", views.leave_community, name="leave_community"),
    path("filter_comments", views.filter_comments, name="filter_comments"),
    path("complete_profile", views.complete_profile, name="complete_profile"),
    path("change_title", views.change_title, name="change_title")
]