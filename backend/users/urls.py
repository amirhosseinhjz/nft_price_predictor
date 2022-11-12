from django.urls import path
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView

app_name = 'users'

urlpatterns = [
    path('', UserRegistrationAPIView.as_view(), name="list"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('token/<key>/', UserTokenAPIView.as_view(), name="token"),
]
