from django.urls import path
from .views import RegisterView, OTPVerifyView, CreateProfileView, LoginView, LoginOTPVerifyView, SearchUserView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-otp/", OTPVerifyView.as_view()),
    path("profile/create/", CreateProfileView.as_view()),
    path("login/", LoginView.as_view()),
    path("login/verify-otp/", LoginOTPVerifyView.as_view()),
    path("profile/search/", SearchUserView.as_view(), name="search-user"),

]