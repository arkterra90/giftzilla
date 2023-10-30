from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *
from .utils import generate_pin

from user.models import *

@login_required
def createRegistry(request):

    if request.method == "POST":
        user = request.user

        f = regForm(request.POST)
        if f.is_valid():
            instance =  f.save(commit=False)
            instance.admin = user
            instance.regPin = generate_pin
            instance.save()
        
        return
    
    else:
        return render(request, "user/createreg.html", {
            "regForm": regForm
        })