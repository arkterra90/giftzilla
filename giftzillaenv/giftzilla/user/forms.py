from django.forms import ModelForm, CharField


from .models import *

class regForm(ModelForm):
    class Meta:
        model = Registry
        fields = "__all__"
        exclude = ["regPin", "admin"]

class giftForm(ModelForm):
    giftUrl = CharField(required=False)
    class Meta:
        model = Gift
        fields = "__all__"
        exclude = ["groupPin", "user"]

class joinForm(ModelForm):
    class Meta:
        model = giftGroups
        fields = "__all__"
        exclude = ["user", "registry"]

class noGiveForm(ModelForm):
    class Meta:
        model = noGive
        fields = "__all__"
        exclude = ["user"]