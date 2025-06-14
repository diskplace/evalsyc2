from django.urls import path
from . import views

urlpatterns=[
    path("make_webinar", views.make_webinar, name="make_webinar"),
    path("webinar_detail/<int:id>/", views.webinar_detail, name="webinar_detail"),
    path("register/<int:id>/", views.register, name="register"),
    
    path("questionaire/<int:id>/", views.questionaire, name="questionaire"),


    path('create_test/<int:id>/', views.create_test, name="create_test"),
    path('redirect_create_test/<int:id>/',views.redirect_create_test, name="redirect_create_test"),
    path("edit_test/<int:id>/", views.edit_test, name="edit_test"),
    path("delete_test/<int:id>/", views.delete_question, name="delete_question"),

    path("display_test/<int:id>/<str:type>", views.display_test, name="display_test"),
    path("eventsdata", views.events_data, name="events_data")
]