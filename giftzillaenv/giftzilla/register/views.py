from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from index.views import home

from .forms import *
from .models import *
from index.utils import send_email
from .utils import generate_pin, send_verify

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
                "message": "Invalid username and/or password. Make sure you have activated your account. Check your email and its spam folder for your activation link."
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
            
            user = User.objects.create_user(username=username, email=email, password=password, is_staff=False, is_superuser=False, is_active=False, last_name=last_name, first_name=first_name)
            user.save()
        except IntegrityError:
            return render(request, "register/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        pin = generate_pin()
        emailPin = emailVerify.objects.create(user=user, pin=pin)
        userID = user.id
        emailverify =  send_verify(emailPin.pin, userID, request)

        if emailverify == 0:
            return render(request, "register/register.html", {
                "message": "Verifcation email was not sent. Please verify email and try again.."
            })


        return HttpResponseRedirect(reverse("index:home"))
    else:
        return render(request, "register/register.html", {
            "UserForm": UserForm,
        })
    

#User can edit their profile info
@login_required
def profileView(request, userID):

    userProf = request.user
    form = UserForm(instance=userProf)

    # prevents logged in user from editting other profiles
    if userID != request.user.id:
        return render(request, "index/404.html")
    
    elif request.method == 'POST':
        f = UserForm(request.POST, instance=userProf)
        if f.is_valid():  
            f.save()
            return render(request, "register/profile.html", {
                "message": "Updates to profile saved.",
                "form": form,
                "userProf": userProf
            })

    else:
        return render(request, "register/profile.html", {
            "form": form,
            "userProf": userProf
        }) 
    

def email_Verify(request, userID, emailPin):

    if request.method == "POST":

        veruserID = request.POST ["userID"]
        veremailPin = request.POST ["emailPin"]

        if str(veruserID) == str(userID) and str(veremailPin) == str(emailPin):

            user = User.objects.get(id=userID)
            user.is_active = True
            user.save()

            return render(request, "register/verify.html", {
                "success": "Success"
            })
        else:
            return render(request, "register/verify.html", {
                "fail": "fail"
            })
    
    else:
        emailVer = emailVerify.objects.get(pin=emailPin)
        user = User.objects.get(id=userID)

        return render(request, "register/verify.html", {
            "user": user,
            "emailVer": emailVer
        })