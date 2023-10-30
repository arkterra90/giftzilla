# Generated by Django 4.2.6 on 2023-10-30 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_registry'),
    ]

    operations = [
        migrations.AddField(
            model_name='registry',
            name='spendLimit',
            field=models.IntegerField(blank=True, null=True, verbose_name='Max Spending Limit:'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='regGroupCap',
            field=models.IntegerField(blank=True, null=True, verbose_name='Max Number of Group Participants:'),
        ),
        migrations.AlterField(
            model_name='registry',
            name='urlNumCap',
            field=models.IntegerField(default=5, verbose_name='Max Number Of Gift Request:'),
        ),
    ]