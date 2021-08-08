from django.urls import path

from zanhu.users.views import (
    UserDetailView,
    UserUpdateView,
)

app_name = "users"
urlpatterns = [
    path("update/", view=UserUpdateView.as_view(), name="update"),
    path("<str:username>/", view=UserDetailView.as_view(), name="detail"),
]
