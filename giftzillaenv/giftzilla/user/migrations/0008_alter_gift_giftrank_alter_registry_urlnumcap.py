# Generated by Django 4.2.6 on 2023-11-04 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_nogive_listpair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='giftRank',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='registry',
            name='urlNumCap',
            field=models.IntegerField(blank=True, default=5, null=True, verbose_name='Max Number Of Gift Request:'),
        ),
    ]
