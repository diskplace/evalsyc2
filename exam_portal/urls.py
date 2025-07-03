from django.urls import path
from . import views

urlpatterns = [
    path('result/<int:id>/',views.display_result, name='display_result'), 
    path("display_result/<int:id>/", views.display_result , name="display_result"),
    path("generate_qr/<int:id>/<str:type>/", views.generate_qr , name="generate_qr"),
    path("qr_evalution/<int:id>/", views.qr_evalution, name="qr_evalution"),
    path("display_qr/<int:id>/<str:type>/", views.display_qr , name="display_qr"),
    path("display_test/<int:id>/<str:type>/", views.display_test , name="display_test"),


    path("create_certificate/<int:id>/", views.create_certificate, name="create_certificate"),
    path("redirect_certificate/<int:id>/", views.redirect_certificate , name="redirect_certificate"),
    path("upload_img/<int:id>/", views.upload_img , name="upload_img"),
    path("cert_preview/<int:id>/", views.cert_preview, name="cert_preview"),

    path("display_qr/<int:id>/", views.display_qr , name="display_qr"),
    path("upload_contents/<int:id>/", views.save_certificate , name="upload_contents"),

]