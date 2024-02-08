from django.urls import path
from .views import login_view
from django.contrib.auth.views import LogoutView

app_name = "Apps.authentication"
urlpatterns = [
    path('accounts/login/', login_view, name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout")
]
