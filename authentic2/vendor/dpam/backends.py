import pam

from django.conf import settings
from django.contrib.auth.models import User

class PAMBackend:
    def authenticate(self, username=None, password=None):
        service = getattr(settings, 'PAM_SERVICE', 'login')
        if pam.authenticate(username, password, service=service):
            try:
                user = User.objects.get(username=username)
            except:
                user = User(username=username, password='not stored here')

                if getattr(settings, 'PAM_IS_SUPERUSER', False):
                  user.is_superuser = True

                if getattr(settings, 'PAM_IS_STAFF', user.is_superuser):
                  user.is_staff = True

                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
