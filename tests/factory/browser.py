from django.conf import settings
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from tests.factory.user import AuthUserFactory


def create_session_cookie():
    """
    Creates a cookie containing a session for a user

    Stolen from https://stackoverflow.com/questions/22494583/login-with-code-when-using-liveservertestcase-with-django
    :param username:
    :param password:
    :return:
    """

    # First, create a new test user
    user = AuthUserFactory()

    # Then create the authenticated session using the new user credentials
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()

    # Finally, create the cookie dictionary
    cookie = {settings.SESSION_COOKIE_NAME: session.session_key}
    return cookie
