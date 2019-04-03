from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Api.as_view()),
    path('rooms', views.RoomsView.as_view()),
    path('register', views.Register.as_view()),
    path('devices',views.DevicesView.as_view())

 ]