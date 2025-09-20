from django.urls import path, include
from . import views


app_name = "users"
urlpatterns = [
    path("", views.home),
    path("logout", views.logout_view),
    
    ]