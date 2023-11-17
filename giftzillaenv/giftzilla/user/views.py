from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .forms import *
from .utils import generate_pin, regPairs

from user.models import *

# Allows an admin to make adjustments to their registry info
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

        if instance.regGroupCap == '':
            instance.regGroupCap = None

        instance.save()

        return HttpResponseRedirect(reverse('user:adminReg', args=[groupPin]))
    
    # Queries for user admin registry and sends info to template
    else:
        reg = Registry.objects.get(regPin=groupPin)
        reginstance = regForm(instance=reg)

        regPart = giftGroups.objects.filter(groupPin=groupPin)

        try:
            pairs = listPair.objects.filter(regPin=groupPin)
        except ObjectDoesNotExist:
            pairs = None

        return render(request, "user/adminreg.html", {
            "reginstance": reginstance,
            "reg": reg,
            "regPart": regPart,
            "pairs": pairs
        })
    
# Allows an admin to view a wish list from someone who
# has joined their registry.
@login_required
def adminWishListView(request, userID, groupPin):

    gifts = Gift.objects.filter(user=userID, groupPin=groupPin)
    reg = Registry.objects.get(regPin=groupPin)
    try:
        noPair = noGive.objects.get(user=userID, regPin=groupPin)
    except ObjectDoesNotExist:
        noPair = None
    return render(request, "user/adminwishview.html", {
        "reg": reg,
        "gifts": gifts,
        "noPair": noPair
    })

# Allows admin to create pairs
@login_required
def createPairs(request, groupPin):
    
    reg =  Registry.objects.get(regPin=groupPin)
    noPairs = noGive.objects.filter(regPin=groupPin).values_list('user__id', 'noGift__id')
    people = giftGroups.objects.filter(groupPin=groupPin).values_list('user__id', flat=True)

    try:
        pairs = listPair.objects.filter(regPin=groupPin)
    except ObjectDoesNotExist:
        pairs = None

    if request.method ==  "POST":

        if pairs != None:
            pairs.delete()
        # Utils function to create pairs
        j = regPairs(people, noPairs)

        # In the event the function returns None. Handles error.
        if j == None:
            return render(request, "user/createpairs.html", {
                "reg": reg,
                "message": "Not able to make pairs at this time. Please try again."
            })

        # Creates listPair entries for user pairings
        for p in j:

            userFrom = User.objects.get(id=p[0])
            userTo = User.objects.get(id=p[1])

            t = listPair.objects.create(giver=userFrom, reciever=userTo, regPin=groupPin)
            try:
                pairs = listPair.objects.filter(regPin=groupPin)
            except ObjectDoesNotExist:
                pairs = None
        return render(request, "user/createpairs.html", {
            "reg": reg,
            "pairs": pairs,
            "message": "Pairs created successfully."
        })
    
    else:
    
        return  render(request, "user/createpairs.html",{
            "reg": reg,
            "pairs": pairs
        })

# Allows a user to create a new registry.
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
            joinGroup = giftGroups(user=user, groupPin=newGroupPin, registry=regSuccess)
            joinGroup.save()

        return render(request, "user/regsuccess.html", {
            "regSuccess": regSuccess
        })
    
    else:
        return render(request, "user/createreg.html", {
            "regForm": regForm
        })
    
# Allows an admin to delete an entire registry
@login_required
def regDelete(request, groupPin):
    
    reg = Registry.objects.get(regPin=groupPin)

    if request.method == "POST":

        
        reg.delete()
        userID = request.user.id
        
        return HttpResponseRedirect(reverse('user:viewReg', args=[userID]))

    else:
        return render(request, "user/regdelete.html", {
            "reg": reg
        })

# Allows a user to join a registry.
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
                    instance.registry = Registry.objects.get(regPin=pin)
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
    
# Unfinished
@login_required
def regPair(request, groupPin):

    reg = Registry.objects.filter(regPin=groupPin)
    regUsers = giftGroups.objects.filter(groupPin=groupPin)
    noPairs = noGive.objects.filter(regPin=groupPin)


    return

# Saves user wish list for a registry they are a part of.
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

        giftForms = []

        for i in range(urlCap):
            form = giftForm(request.POST, prefix=f'gift_form_{i}')
            giftForms.append(form)

        # if not currentGift.exists():
        try:
            if all(form.is_valid() for form in giftForms):
                for form in giftForms:
                    gift = form.save(commit=False)
                    gift.user = user 
                    gift.groupPin = groupReg.regPin
                    gift.save()
        
        # Saves user selection for someone they can't be paired with

            return render(request, "user/usergifts.html", {
                "message": "Wish list saved.",
                "success":  "success",
                "groupReg": groupReg,
                "user": user,
                "giftForms": giftForms,
                })
        
        except TypeError:


            return render(request, "user/usergifts.html", {
            "groupReg": groupReg,
            "user": user,
            "giftForms": giftForms,
            "message": "Something went wrong saving your wish list. Please try again."
        })
    
    else:
        groupReg = Registry.objects.get(regPin=groupPin)
        user = User.objects.get(id=userID)
        urlCap = groupReg.urlNumCap
        regUsers = giftGroups.objects.filter(groupPin=groupPin)

        giftForms = []

        for i in range(urlCap):
            giftForms.append(giftForm(prefix=f'gift_form_{i}'))

        noForm = noGiveForm()
        noForm.fields['noGift'].queryset = regUsers
        
        return render(request, "user/usergifts.html", {
            "groupReg": groupReg,
            "user": user,
            "giftForms": giftForms,
            
        })

# Allows user to delete themselves from a registry.
@login_required
def userRegDelete(request, userID, groupPin):

    if request.method == "POST":

        user = request.user

        try:
            userGiftGroup = giftGroups.objects.get(user=user, groupPin=groupPin)
            userGiftGroup.delete()
        except ObjectDoesNotExist:
            pass

        try:
            userWishList = Gift.objects.filter(user=user, groupPin=groupPin)
            userWishList.delete()
        except ObjectDoesNotExist:
            pass

        try:
            userNoPair = noGive.objects.filter(user=user, regPin=groupPin)
            userNoPair.delete()
        except ObjectDoesNotExist:
            pass

        return HttpResponseRedirect(reverse('user:viewReg', args=[userID]))
    
    else:

        reg = giftGroups.objects.get(user=request.user, groupPin=groupPin)
        return render(request, "user/userRegDel.html", {
            "reg": reg,
        })
    

# Gives user a view of all registries they admin or have registered for.
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
            Gifts = Gift.objects.filter(user=user).values_list('groupPin', flat=True).distinct()
        except ObjectDoesNotExist:
            Gifts = None
       
        return render(request, "user/viewreg.html", {
            "adminRegs": adminRegs,
            "joinedRegs": joinedRegs,
            "gifts": Gifts,
           
        })
    
# Allows user to view their wishlist from a specific registry
@login_required
def viewWishList(request, userID, groupPin):

    regDetail =  Registry.objects.get(regPin=groupPin)
    user = User.objects.get(id=userID)
    regWishList = Gift.objects.filter(groupPin=groupPin, user=user)
    noPair = noGive.objects.filter(regPin=groupPin, user=user)

    if request.method == "POST":
        return
    
    else:

        return render(request, "user/wishlist.html", {
            "regDetail": regDetail,
            "regWishList": regWishList,
            "noPair": noPair
        })
    
# Allows user to edit an individual gift wish 
@login_required
def wishEdit(request, wishID):

    gift = Gift.objects.defer('user').get(id=wishID)
    giftinstance = giftForm(instance=gift)

    if request.method == "POST":
        instance = gift

        instance.giftUrl = request.POST.get("giftUrl")
        instance.giftRank = request.POST.get("giftRank")
        
        if instance.giftRank == '':
            instance.giftRank = None
        
        try:
            instance.save()
        except (DatabaseError, IntegrityError):
            return render(request, "user/wishedit.html", {
            "gift": gift,
            "giftinstance": giftinstance,
            "message": "Changes Not Saved! Please try again."
        }) 

        gift = Gift.objects.defer('user').get(id=wishID)
        giftinstance = giftForm(instance=gift)

        return render(request, "user/wishedit.html", {
            "gift": gift,
            "giftinstance": giftinstance,
            "message": "Changes Saved!"
        })
    
    else:
        return render(request, "user/wishedit.html", {
            "gift": gift,
            "giftinstance": giftinstance
        })