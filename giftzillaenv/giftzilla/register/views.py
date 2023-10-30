from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from index.views import home

from .forms import *
from .models import *



# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index:home'))
        else:
            return render(request, "register/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "register/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index:home'))

# Registers a new user.
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name  = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["emailAddress"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["verifyPassword"]
        if password != confirmation:
            return render(request, "register/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            
            user = User.objects.create_user(username=username, email=email, password=password, is_staff=False, is_superuser=False, is_active=True, last_name=last_name, first_name=first_name)
            user.save()
        except IntegrityError:
            return render(request, "register/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register/register.html", {
            "UserForm": UserForm,
        })