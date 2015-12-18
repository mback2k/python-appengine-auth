Remote Google App Engine OAuth backend for Django
=================================================

[Python-AppEngine-Auth](https://github.com/mback2k/python-appengine-auth) is an
extension to [Python-Social-Auth](https://github.com/omab/python-social-auth)
which adds a OAuth backend for Google App Engine based Google Accounts.

This application makes use of the
[Google App Engine OAuth Profile endpoint application](https://github.com/mback2k/appengine-oauth-profile)
which is by default hosted at https://oauth-profile.appspot.com/

Dependencies
------------
- python-social-auth [https://github.com/omab/python-social-auth]
- requests-oauthlib  [https://github.com/requests/requests-oauthlib]

Installation
------------
Install the latest version from pypi.python.org:

    pip install python-appengine-auth

Install the development version by cloning the source from github.com:

    pip install git+https://github.com/mback2k/python-appengine-auth.git

Configuration
-------------
Add the package to your `INSTALLED_APPS`:

    INSTALLED_APPS += (
        'social.apps.django_app.default',
        'social_appengine_auth',
    )

Add the desired backends to your `AUTHENTICATION BACKENDS`:

    AUTHENTICATION_BACKENDS += (
        'social_appengine_auth.backends.GoogleAppEngineOAuth',
        'social_appengine_auth.backends.GoogleAppEngineOAuth2',
    )

Add the pipeline to your `SOCIAL_AUTH_PIPELINE`:

    SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_details',
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',
        # Add the following custom pipeline:
        'social_appengine_auth.pipelines.associate_by_user_id',
        # 'social.pipeline.mail.mail_validation',
        # 'social.pipeline.social_auth.associate_by_email',
        'social.pipeline.user.create_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details',
    )

Additional Settings
-------------------
Add some or all of the following settings to your `settings.py`:

    # Hostname of the OAuth and Web Service endpoint
    SOCIAL_AUTH_GOOGLE_APPENGINE_OAUTH_SERVER = 'oauth-profile.appspot.com'

    # Use static and unique Google App Engine user's user_id as identifier
    # Defaults to False which makes it use the user's email address
    GOOGLE_APPENGINE_OAUTH_USE_UNIQUE_USER_ID = True

    # Setup Google OAuth 1.0 consumer key and secret
    SOCIAL_AUTH_GOOGLE_APPENGINE_OAUTH_KEY = ''
    SOCIAL_AUTH_GOOGLE_APPENGINE_OAUTH_KEY = ''

    # or Setup Google OAuth 2.0 client id and secret
    SOCIAL_AUTH_GOOGLE_APPENGINE_OAUTH2_KEY = ''
    SOCIAL_AUTH_GOOGLE_APPENGINE_OAUTH2_SECRET = ''

Please refer to the [Python-Social-Auth](http://psa.matiasaguirre.net/)
documentation for additional information.

License
-------
* Released under MIT License
* Copyright (c) 2012-2015 Marc Hoersken <info@marc-hoersken.de>
