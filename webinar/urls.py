from django.urls import path
from . import views

urlpatterns=[
    path("make_webinar", views.make_webinar, name="make_webinar"),
    path("webinar_detail/<int:id>/", views.webinar_detail, name="webinar_detail"),
    path("register/<int:id>/", views.register, name="register"),
    path("questionaire/<int:id>/", views.questionaire, name="questionaire"),
    path('result/<int:id>/',views.average_result, name="result")
    
]