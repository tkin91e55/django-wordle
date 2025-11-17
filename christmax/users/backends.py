from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.urls import resolve, Resolver404

User = get_user_model()

class AdminUsernameBackend(ModelBackend):
    """
    Allow authentication with username OR email.
    ONLY for staff users accessing admin pages.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            if not user.is_staff:
                return None

            if request and hasattr(request, 'path'):
                try:
                    resolved = resolve(request.path)
                    if resolved.namespace == 'admin':
                        return user
                except Resolver404:
                    pass

            return None

        return None
