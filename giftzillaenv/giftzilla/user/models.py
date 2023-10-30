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
    giftUrl = models.URLField()
    giftRank = models.CharField(max_length=1, choices=Rank)

    def __str__(self):
        return f"{self.groupPin} {self.user} {self.giftUrl} {self.giftUrl}"


class giftGroups(models.Model):
    groupPin = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.groupPin} {self.user}"

class Registry(models.Model):
    regPin = models.CharField(max_length=5)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    urlNumCap = models.IntegerField(default=5, verbose_name="Max Number Of Gift Request:")
    spendLimit = models.IntegerField(blank=True, null=True, verbose_name="Max Spending Limit:")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    regGroupCap = models.IntegerField(blank=True, null=True, verbose_name="Max Number of Group Participants:")

    def __str__(self):
        return f"{self.regPin} {self.admin} {self.urlNumCap} {self.notes} {self.regGroupCap}"
