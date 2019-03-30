from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.Upload.as_view()),
    path('gallery', views.Gallery.as_view()),
]
