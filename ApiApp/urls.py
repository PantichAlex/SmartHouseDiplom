from django.urls import path, include


from . import views

urlpatterns = [
    path('', views.Api.as_view()),
    path('rooms', views.RoomsView.as_view()),
    path('register', views.Register.as_view()),
    path('devices',views.DevicesView.as_view()),
    path('devices/<int:id>', views.DeviceView.as_view()),
    path('login', views.Login.as_view()),
    path('users', views.UsersView.as_view()),
    path('users/<int:id>', views.UserView.as_view()),
    path('permissions', views.PermissionsView.as_view()),
    path('permissions/<int:id>',views.PermissionView.as_view())


 ]