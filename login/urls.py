from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("verification", views.generate_otp, name="otp"),
    path("admin_panel", views.admin_panel, name="admin_panel"),
    path("user_dashboard", views.user_dashboard, name="user_dashboard")

]