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
from .models import *

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
            }, status=401)
        elif User.objects.filter(email=email).exists():
            return Response({
                "status": "error",
                "detail": "Email is exist"
            }, status=401)
        
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


########## Goods Start ###########
class AdView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        ads = Ad.objects.all()
        return Response({
            "status": "success",
            "data": [{
                "id": ad.goods.id,
                "title": ad.goods.title,
                "price": ad.goods.price,
                "creator": {
                    "id": ad.goods.user.id,
                    "name": ad.goods.user.store.name
                },
                "images": [image.url for image in GoodsImage.objects.filter(goods__id=ad.goods.id)],
                "like": False
            } for ad in ads]
        })
        
        
class GoodsOfCategoryView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        category = Category.objects.get(name=request.data["category"])
        goods = Goods.objects.filter(category=category)
        result = []
        for g in goods:
            if g.publish:
                result.append({
                    "id": g.id,
                    "title": g.title,
                    "price": g.price,
                    "creator": {
                        "id": g.user.id,
                        "name": g.user.store.name
                    },
                    "images": [image.url for image in GoodsImage.objects.filter(goods__id=g.id)],
                    "like": False
                })
        return Response({
            "status": "success",
            "data": result
        })


class GoodsView(generics.RetrieveAPIView):
    def get(self, request, id, *args, **kwargs):
        try:
            goods = Goods.objects.get(pk=id)
            return Response({
                "status": "success",
                "data": {
                    "id": goods.id,
                    "title": goods.title,
                    "price": goods.price,
                    "creator": {
                        "id": goods.user.id,
                        "name": goods.user.store.name
                    },
                    "images": [image.url for image in GoodsImage.objects.filter(goods__id=goods.id)],
                    "like": False
                }
            })
        except Goods.DoesNotExist:
            return Response({
                "status": "error",
                "detail": "Goods not found"
            })
    

class GoodsSearchView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        goods = Goods.objects.filter(title__contains=request.data["keyword"])
        return Response({
            "status": "success",
            "data": [{
                    "id": g.id,
                    "title": g.title,
                    "price": g.price,
                    "creator": {
                        "id": g.user.id,
                        "name": g.user.store.name
                    },
                    "images": [image.url for image in GoodsImage.objects.filter(goods__id=g.id)],
                    "like": False
                } for g in goods]
        })
########## Goods End ###########


########## Goods-consumer Start ###########

########## Goods-consumer End ###########


########## Goods-seller Start ###########
########## Goods-seller End ###########


########## Others Start ###########
class CategoryView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return Response({
            "status": "success",
            "data": [category.name for category in categories]
        })
########## Others End ###########