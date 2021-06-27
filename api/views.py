# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.utils import timezone

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied

import json

from django.contrib.auth.models import User
from .models import Profile

from .serializers import AuthSerializer


class RetriveDocView(generics.RetrieveAPIView):
    # authentication_classes = [BasicAuthentication,TokenAuthentication]
    def retrieve(self, request, *args, **kwargs):
        HOST = request.get_host()
        data = {
            'auth': {
                'description': '帳戶相關功能',
                'url': ('{}/api/v1/auth'.format(HOST)),
            },
        }
        if request.auth:
            data['is_auth'] = True
        else:
            data['is_auth'] = False
        return Response(data)


########## Auth Start ###########

class AuthView(TokenViewBase):
    serializer_class = AuthSerializer


class UserCreateView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        
        if User.objects.filter(username=username).exists():
            return Response({
                "status": "error",
                "detail": "Username is exist"
            })
        elif User.objects.filter(email=email).exists():
            return Response({
                "status": "error",
                "detail": "Email is exist"
            })
        
        user = User.objects.create_user(username, email, password)
        user.save()
        profile = Profile(nick_name="", user=user)
        profile.avatar = profile.avatar_url()
        profile.save()
        return Response({
            'status': 'success',
        })


class TokenVerifyView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        # print(request.auth)
        data = {
            'status': 'success',
            'user': str(request.user),
            'auth_token': str(request.auth),
            'auth': "True",
        }
        return Response(data)


class UserProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = {
            'status': 'success',
            'username': str(request.user.username),
            'first_name': str(request.user.first_name),
            'last_name': str(request.user.last_name),
            'email': str(request.user.email),
            'avatar': str(request.user.profile.avatar),
            'nick_name': str(request.user.profile.nick_name),
        }
        return Response(data)
    
    def put(self, request, *args, **kwargs):
        return Response({
            'status': 'success',
        })
    
    def patch(self, request, *args, **kwargs):
        return Response({
            'status': 'success',
        })

########## Auth End ###########
