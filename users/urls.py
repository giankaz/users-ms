from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.ListCreateUserView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("users/<pk>/", views.RetrieveUpdateDestroyUserView.as_view()),
    path("users/reactivate/<uuid:user_id>/", views.ReactivateView.as_view()),
]
