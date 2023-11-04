from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist



from .models import *
from .forms import *
from .utils import generate_pin

from user.models import *

@login_required
def adminReg(request, groupPin):
    return

@login_required
def createRegistry(request):

    if request.method == "POST":
        user = request.user

        f = regForm(request.POST)
        if f.is_valid():
            instance =  f.save(commit=False)
            instance.admin = user
            newGroupPin = generate_pin()
            instance.regPin = newGroupPin
            instance.save()

            # Gives user feedback on their unique group pin and info
            regSuccess = Registry.objects.get(regPin=newGroupPin)

            # Admin should be auto added to their own reg.
            joinGroup = giftGroups(user=user, groupPin=newGroupPin)
            joinGroup.save()

        return render(request, "user/regsuccess.html", {
            "regSuccess": regSuccess
        })
    
    else:
        return render(request, "user/createreg.html", {
            "regForm": regForm
        })
    
@login_required
def regJoin(request, userID):

    if request.method == "POST":
    
        user = User.objects.get(id=userID)
        f = joinForm(request.POST)
        if f.is_valid():
            instance = f.save(commit=False)
            instance.user = user
            pin = instance.groupPin

            # Makes sure user doesn't join the same reg twice
            try: 
                exist = giftGroups.objects.get(groupPin=pin, user=user)
                if exist != None:
                    return render(request, 'user/joinreg.html', {
                        "joinForm": joinForm,
                        "message": "You have already joined that registry. Go to View Registries to get more details."
                    })
            
            # If user has not already joined reg user joining can move forward
            except ObjectDoesNotExist:

            # makes sure the registry pre-exist in the data base
                try:
                    Registry.objects.get(regPin=pin)
                    instance.save()
                    return render(request, 'user/joinreg.html', {
                        "message": "Success group joined. Check View Registries to see group."
                    })
                
                except ObjectDoesNotExist:
            
                    return render(request, "user/joinreg.html", {
                        "joinForm": joinForm,
                        "message": "Group does not exist. Try again"
                    })
        
    else:

        return render(request, "user/joinreg.html", {
            "joinForm": joinForm
        })
    
@login_required
def viewReg(request, userID):

    # Prevents user from accessing other registries when logged in.
    if userID != request.user.id:
        return render(request, "index/404.html")
    else:
        user = User.objects.get(id=userID)

        # Get all admined and joined registries
        try:
            adminRegs = Registry.objects.filter(admin=user)
        except ObjectDoesNotExist:
            adminRegs = None
        try:
            joinedRegs = giftGroups.objects.filter(user=user)
        except ObjectDoesNotExist:
            joinedRegs = None

        return render(request, "user/viewreg.html", {
            "adminRegs": adminRegs,
            "joinedRegs": joinedRegs
        })