from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

import logging

log = logging.getLogger(__name__)


def login_view(request):
    return render(request, "login/login_page.html")


def login_request(request):
    if request.method == "POST":
        log.debug("Login view POST")
        print(request.POST)
        username = request.POST.get("email")
        password = request.POST.get("password")
        log.debug("Username: " + username)
        log.debug("Password: " + password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shared:home")
        return render(request, "login/login_page.html",
                      {'error': 'Unless you are a Django admin, please sign in with Google.'})
    return render(request, "shared/404.html")
