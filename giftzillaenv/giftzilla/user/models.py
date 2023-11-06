from django.db import models
from register.models import *

Rank = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3')
)
# Create your models here.
class Gift(models.Model):
    groupPin = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    giftUrl = models.URLField(blank=True, null=True)
    giftRank = models.CharField(max_length=1, choices=Rank, blank=True, null=True)

    def __str__(self):
        return f"{self.groupPin} {self.user} {self.giftUrl} {self.giftUrl}"


class Registry(models.Model):
    regPin = models.CharField(max_length=5)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    regName = models.CharField(max_length=25, verbose_name="Registry Group Name:")
    urlNumCap = models.IntegerField(default=5, verbose_name="Max Number Of Gift Request:", blank=True, null=True)
    spendLimit = models.IntegerField(blank=True, null=True, verbose_name="Max Spending Limit:")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    regGroupCap = models.IntegerField(blank=True, null=True, verbose_name="Max Number of Group Participants:")

    def __str__(self):
        return f"{self.regPin} {self.admin} {self.urlNumCap} {self.notes} {self.regGroupCap} {self.spendLimit} {self.regName}"

class giftGroups(models.Model):
    groupPin = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registry = models.ForeignKey(Registry, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.groupPin} {self.user} {self.registry}"
    
# Model to allow users to select a person in their registry they cannot give a gift to such as a spouse. 
class noGive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nogive_user')
    noGift = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nogive_noGift', verbose_name="User to not pair with:")
    regPin = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.user} {self.noGift} {self.regPin}"
    
class listPair(models.Model):
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listpair_giver')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listpair_reciever')
    regPin = models.CharField(max_length=5)


    def __str__(self):
        return f"{self.giver} {self.reciever} {self.regPin}"