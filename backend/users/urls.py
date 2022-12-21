from django.urls import path
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserSessionLoginAPIView

app_name = 'users'

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view(), name="list"),
    path('session-login/', UserSessionLoginAPIView.as_view(), name="api-auth-login"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('token/<key>/', UserTokenAPIView.as_view(), name="token"),
]
