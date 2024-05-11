from django.urls import path
from . import views
app_name = "main"
urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("success/", views.success_view, name="success"),
    path("submission/", views.submission_view, name="submission"),
    path("signup/", views.signup_view, name="signup"),
    path("reviewreports/", views.reviewreports_view, name="reviewreports_view"),
    path("profile/", views.profile_view, name="profile"),
    path("deletesubmission/<int:pk>", views.delete_submission, name="delete_submission"),
]
