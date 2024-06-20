from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# https://stackoverflow.com/questions/37332190/django-login-with-email
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None