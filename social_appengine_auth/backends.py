# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from social.backends.google import GoogleOAuth, GoogleOAuth2


# Google OAuth base configuration
GOOGLE_OAUTH_SERVER = setting('GOOGLE_APPENGINE_OAUTH_SERVER', 'oauth-profile.appspot.com')
AUTHORIZATION_URL = 'https://%s/_ah/OAuthAuthorizeToken' % GOOGLE_OAUTH_SERVER
REQUEST_TOKEN_URL = 'https://%s/_ah/OAuthGetRequestToken' % GOOGLE_OAUTH_SERVER
ACCESS_TOKEN_URL = 'https://%s/_ah/OAuthGetAccessToken' % GOOGLE_OAUTH_SERVER

GOOGLE_APPENGINE_PROFILE_V1 = 'https://%s/oauth/v1/userinfo' % GOOGLE_OAUTH_SERVER
GOOGLE_APPENGINE_PROFILE_V2 = 'https://%s/oauth/v2/userinfo' % GOOGLE_OAUTH_SERVER


# Backends
class BaseGoogleAppEngineAuth(object):
    def get_user_id(self, details, response):
        """Use Google user_id as unique id"""
        return response['id']

    def get_user_details(self, response):
        """Return user details from OAuth Profile Google App Engine App"""
        email = response['email']
        username = response.get('nickname', email).split('@', 1)[0]
        return {'username': username,
                'email': email,
                'fullname': '',
                'first_name': '',
                'last_name': ''}


class GoogleAppEngineOAuthBackend(BaseGoogleAppEngineAuth, GoogleOAuth):
    """Google App Engine OAuth authorization mechanism"""
    name = 'google-appengine-oauth'
    AUTHORIZATION_URL = AUTHORIZATION_URL
    REQUEST_TOKEN_URL = REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = ACCESS_TOKEN_URL
    SETTINGS_KEY_NAME = 'GOOGLE_APPENGINE_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'GOOGLE_APPENGINE_CONSUMER_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Load user data from OAuth Profile Google App Engine App"""
        url = GOOGLE_APPENGINE_PROFILE_V1
        auth = self.oauth_auth(access_token)
        return self.get_json(url,
            auth=auth, params=auth
        )


class GoogleAppEngineOAuth2(BaseGoogleAppEngineAuth, GoogleOAuth2):
    """Google App Engine OAuth2 authorization backend"""
    name = 'google-appengine-oauth2'
    USE_DEPRECATED_API = True
    SETTINGS_KEY_NAME = 'GOOGLE_APPENGINE_CLIENT_ID'
    SETTINGS_SECRET_NAME = 'GOOGLE_APPENGINE_CLIENT_SECRET'

    def user_data(self, access_token, *args, **kwargs):
        """Load user data from OAuth Profile Google App Engine App"""
        url = GOOGLE_APPENGINE_PROFILE_V2
        return self.get_json(url, headers={
            'Authorization': 'Bearer ' + access_token
        })
