# Generated by Django 4.2.6 on 2023-11-06 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0012_alter_gift_gifturl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nogive',
            name='noGift',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='nogive_noGift', to=settings.AUTH_USER_MODEL, verbose_name='User to not pair with:'),
        ),
    ]
