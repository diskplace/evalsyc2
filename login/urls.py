from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("verification", views.generate_otp, name="otp"),
  

    path("admin_calendar",views.admin_calendar, name="admin_calendar"),
    path("admin_certificate",views.admin_certificate, name="admin_certificate"),
    path("admin_events",views.admin_events, name="admin_events"),
    path("admin_setting",views.admin_setting, name="admin_setting"),
    path("admin_users",views.admin_users, name="admin_users"),
    path("admin_events",views.admin_events, name="admin_events"),


    path("user_dashboard", views.user_dashboard, name="user_dashboard"),
    path("calendar", views.calendar, name="calendar"),
    path("evaluation_nav", views.evaluation_nav, name="evaluation_nav"),
    path("attendance", views.attendance, name="attendance"),
    path("certificate", views.certificate, name="certificate"),
    path("aboutus", views.aboutus, name="aboutus"),
    path("user_setting", views.user_setting, name="user_setting"),

    path("register_user", views.register_user, name="register_user"),
    path("create_admin", views.create_admin, name="create_admin"),
    path('delete_user/<int:id>/', views.delete_user, name="delete_user"),

    path("generete_authorization_key", views.generete_authorization_key, name="generete_authorization_key"),
    path("edit_user", views.edit_user, name="edit_user"),

    path("Change_password", views.change_password, name="change_password"),



    

    
]