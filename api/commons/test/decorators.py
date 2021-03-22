from functools import wraps
from typing import Callable

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def login(username: str, inject_user: bool = False):
    """
    Login decorator.

    `inject_user` - if True, decorated function will be given `user` argument right after `self`.
    """

    def decor(f: Callable):
        @wraps(f)
        def inner(self, *args, **kwargs):
            user = User.objects.get(username=username)
            refresh_token = RefreshToken.for_user(user)
            self.client.credentials(HTTP_AUTHORIZATION=f'JWT {refresh_token.access_token}')

            if inject_user:
                return f(self, user, *args, **kwargs)
            return f(self, *args, **kwargs)

        return inner

    return decor


def logout():
    """
    Logout decorator.
    """

    def decor(f: Callable):
        @wraps(f)
        def inner(self, *args, **kwargs):
            self.credentials()
            return f(self, *args, **kwargs)

        return inner

    return decor
