from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .forms import *
from .utils import generate_pin

from user.models import *

@login_required
def adminReg(request, groupPin):

    # Updates registry details
    if request.method == "POST":

        instance = Registry.objects.get(regPin=groupPin)

        instance.regName = request.POST.get("regName")
        instance.urlNumCap = request.POST.get("urlNumCap")
        instance.spendLimit = request.POST.get("spendLimit")
        instance.notes = request.POST.get("notes")
        instance.regGroupCap = request.POST.get("regGroupCap")

        instance.save()

        return HttpResponseRedirect(reverse('user:adminReg', args=[groupPin]))
    
    # Queries for user admin registry and sends info to template
    else:
        reg = Registry.objects.get(regPin=groupPin)
        reginstance = regForm(instance=reg)

        regPart = giftGroups.objects.filter(groupPin=groupPin)

        return render(request, "user/adminreg.html", {
            "reginstance": reginstance,
            "reg": reg,
            "regPart": regPart
        })

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
def userGifts(request, groupPin, userID):

    # Makes sure a logged in user cannot alter another users list
    if userID != request.user.id:
        return render(request, "index/404.html")
    
    # Saves users wish list urls and 
    elif request.method == "POST":
        groupReg = Registry.objects.get(regPin=groupPin)
        user = User.objects.get(id=userID)
        urlCap = groupReg.urlNumCap
        currentGift = Gift.objects.filter(groupPin=groupPin, user=user)        

        giftForms = []

        for i in range(urlCap):
            form = giftForm(request.POST, prefix=f'gift_form_{i}')
            giftForms.append(form)

        # if not currentGift.exists():

        if all(form.is_valid() for form in giftForms):
            for form in giftForms:
                gift = form.save(commit=False)
                gift.user = user 
                gift.groupPin = groupReg.regPin
                gift.save()
        
        # Saves user selection for someone they can't be paired with
        try:
            noPair = int(request.POST.get("user_dropdown"))
            
            if noPair == 0:
                t = noGive.objects.create(user=user, noGift=None, regPin=groupPin)
                t.save()
            else:
                p = User.objects.get(id=noPair)
                t = noGive.objects.create(user=user, noGift=p, regPin=groupPin)
                t.save()

            regUsers = giftGroups.objects.filter(groupPin=groupPin)
            noForm = noGiveForm()
            noForm.fields['noGift'].queryset = regUsers

            return render(request, "user/usergifts.html", {
                "message": "Wish list saved.",
                "groupReg": groupReg,
                "user": user,
                "giftForms": giftForms,
                "regUsers": regUsers,
                "noGiveForm": noForm,
                })
        
        except TypeError:

            regUsers = giftGroups.objects.filter(groupPin=groupPin)
            noForm = noGiveForm()
            noForm.fields['noGift'].queryset = regUsers

            return render(request, "user/usergifts.html", {
            "groupReg": groupReg,
            "user": user,
            "giftForms": giftForms,
            "regUsers": regUsers,
            "noGiveForm": noForm,
            "message": "Something went wrong saving your wish list. Please try again."
        })

        # else:

        #     for i in range(urlCap):
        #         form = giftForm(request.POST, prefix=f'gift_form_{i}')
        #         if form.is_valid():
        #             gift = currentGift[i]  # Assuming currentGift contains all existing entries
        #             gift.user = user 
        #             gift.groupPin = groupReg.regPin
        #             gift.save()

        #         regUsers = giftGroups.objects.filter(groupPin=groupPin)
        #         noForm = noGiveForm()
        #         noForm.fields['noGift'].queryset = regUsers

        #         return render(request, "user/usergifts.html", {
        #             "message": "Wish list updated.",
        #             "groupReg": groupReg,
        #             "user": user,
        #             "giftForms": giftForms,
        #             "regUsers": regUsers,
        #             "noGiveForm": noForm,
        #             })
    
    else:
        groupReg = Registry.objects.get(regPin=groupPin)
        user = User.objects.get(id=userID)
        urlCap = groupReg.urlNumCap
        regUsers = giftGroups.objects.filter(groupPin=groupPin)

        noPair = noGive.objects.get(user=user)
       

        giftForms = []

        for i in range(urlCap):
            giftForms.append(giftForm(prefix=f'gift_form_{i}'))

        noForm = noGiveForm()
        noForm.fields['noGift'].queryset = regUsers
        
        return render(request, "user/usergifts.html", {
            "groupReg": groupReg,
            "user": user,
            "giftForms": giftForms,
            "regUsers": regUsers,
            "noGiveForm": noForm,
            "noPair": noPair
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
        try:
            Gifts = Gift.objects.filter(user=user)
        except ObjectDoesNotExist:
            Gifts = None
        try:
            noPair = noGive.objects.filter(user=user)
        except ObjectDoesNotExist:
            noPair = None

        return render(request, "user/viewreg.html", {
            "adminRegs": adminRegs,
            "joinedRegs": joinedRegs,
            "gifts": Gifts,
            "noPair": noPair
        })