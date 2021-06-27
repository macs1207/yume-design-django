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
    path('goods', views.GoodsOfCategoryView.as_view()),  # GET
    path('search', views.GoodsSearchView.as_view()),  # GET
    
    
    
    
    # Others
    path('category', views.CategoryView.as_view()),  # GET

    # # Competition
    # path('competition', views.CompetitionsView.as_view()),  # POST, GET
    # path('competition/join', views.CompetitionJoinView.as_view()),  # GET, POST
    # # GET, PATCH, DELETE
    # path('competition/<str:id>', views.CompetitionView.as_view()),
    # path('competition/<str:id>/player',
    #      views.CompetitionPlayerView.as_view()),  # GET
    # path('competition/<str:id>/match',
    #      views.CompetitionMatchView.as_view()),  # GET, POST
    # path('competition/<str:id>/generate/code',
    #      views.CodeCreateView.as_view()),  # POST

    # # Game
    # path('game', views.GamesView.as_view()),  # GET
    # path('game/<str:name>', views.GameView.as_view()),  # GET
    # path('game/<str:name>/rank', views.RankOfGameView.as_view()),  # GET
    # path('game/<str:name>/code', views.CodeOfGameView.as_view()),  # GET, POST
    # # GET, POST, PATCH, DELETE
    # path('game/code/<str:id>', views.CodeView.as_view()),

    # # Match
    # path('match/<str:id>', views.MatchView.as_view()),  # GET, PATCH
    # path('match/<str:id>/play', views.MatchPlayView.as_view()),  # POST

    # # Service
    # path('service/desire', views.CompetitionView.as_view()),  # POST
    # path('service/issue', views.CompetitionView.as_view()),  # POST

    # # Utilitys
    # path('file', views.FileView.as_view()),  # POST

]
# router.register('index', views.APIViewSet, basename='name')
