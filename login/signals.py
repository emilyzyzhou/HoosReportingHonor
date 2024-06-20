from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    if user.is_superuser:
        return redirect("login:login_view")
    else:
        return redirect("shared:home")