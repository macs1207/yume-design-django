from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.models import User, Group
from allauth.socialaccount.models import SocialAccount 
# from competition_api.models import Competition

# import json

from rest_framework import serializers, exceptions
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from google.oauth2 import id_token
from google.auth.transport import requests

# class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Competition
#         fields = ['id', 'name', 'game', 'manager']
#         pass


class AuthSerializer(serializers.Serializer):
    type = serializers.CharField()
    account = serializers.DictField()
    
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials'),
        'unknown_auth_type': "Unknown auth type"
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
    
    def verify_token(self, authenticate_args):
        """
        驗證 id_token 是否正確

        token: JWT
        """
        provider = authenticate_args["provider"]
        token = authenticate_args["id_token"]
        
        if provider == "google":
            print(token)
            try:
                idinfo = id_token.verify_oauth2_token(
                    token,
                    requests.Request(),
                    SOCIAL_GOOGLE_CLIENT_ID
                )
                if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    raise exceptions.AuthenticationFailed(
                        self.error_messages['no_active_account'],
                        'no_active_account',
                    )
                # if idinfo['aud'] not in [SOCIAL_GOOGLE_CLIENT_ID]:
                #     raise exceptions.AuthenticationFailed(
                #         self.error_messages['no_active_account'],
                #         'no_active_account',
                #     )
                # Success
                print(idinfo)
                return idinfo
            except ValueError as e:
                print(e)
            except Exception as e:
                print(e)                
        else:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

    def validate(self, attrs):
        if attrs.get('type') == "general":
            authenticate_kwargs = {
                'username': attrs.get('account')['username'],
                'password': attrs.get('account')['password'],
            }
            try:
                authenticate_kwargs['request'] = self.context['request']
            except KeyError:
                pass
            
            self.user = authenticate(**authenticate_kwargs)            

        elif attrs.get('type') == "social":
            authenticate_args = {
                'provider': attrs.get('account')['provider'],
                'id_token': attrs.get('account')['id_token'],
            }
            try:
                authenticate_args['request'] = self.context['request']
            except KeyError:
                pass
            
            idinfo = self.verify_token(authenticate_args)
            print(idinfo)

            # TODO: 第三方登入串接 model
            self.user = User.objects.get(pk=2)
            
        else:
            raise exceptions.AuthenticationFailed(
                self.error_messages['unknown_auth_type'],
                'unknown_auth_type'
            )
            
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
            
        refresh = self.get_token(self.user)

        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
