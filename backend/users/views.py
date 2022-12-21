from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView, RetrieveAPIView
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import json

class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'errors':serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        '''
        Register a new user:
        '''
        return self.create(request, *args, **kwargs)

class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        '''
        Login a user:
        '''
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'errors':serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.user
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            data=TokenSerializer(token).data,
            status=status.HTTP_200_OK,
        )

class UserTokenAPIView(RetrieveAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)

    def get(self, request, key, *args, **kwargs):
        '''
            Delete token for the user. 
        '''
        self.retrieve(request, key, *args, **kwargs)

class UserSessionLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        '''
        This is a session based login. It is not recommended to use this in production.
        '''
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'errors':serializer.errors.values()}, status=status.HTTP_400_BAD_REQUEST)
        serializer.login(request)
        return Response(
            data='Logged in successfully',
            status=status.HTTP_200_OK,
        )

