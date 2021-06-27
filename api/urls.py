from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


app_name = 'api'

urlpatterns = [
    path('', views.RetriveDocView.as_view(), name='api_doc'),

    # Authentication
    path('auth/registration', views.UserCreateView.as_view(), name='user_registration'),  # POST
    path('auth/token', views.AuthView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify', views.TokenVerifyView.as_view(), name='token_verify'),
    path('me', views.UserProfileView.as_view(),
         name='user_profile'),  # GET, PATCH
    
    # Goods
    path('ad', views.AdView.as_view()),  # GET
    path('goods', views.GoodsOfCategoryView.as_view()),  # POST
    path('goods/<int:id>', views.GoodsView.as_view()),  # GET
    path('search', views.GoodsSearchView.as_view()),  # POST
    
    # Goods-consumer
    path('cart', views.CartView.as_view()), # GET, POST, PATCH, DELETE
    
    # Others
    path('category', views.CategoryView.as_view()),  # GET

]
# router.register('index', views.APIViewSet, basename='name')
