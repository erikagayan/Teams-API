from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, CreateTokenView, ManageUserView, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("", include(router.urls)),
]

app_name = "users"
