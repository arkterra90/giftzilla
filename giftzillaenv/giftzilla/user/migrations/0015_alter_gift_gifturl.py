# Generated by Django 4.2.6 on 2023-11-12 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_nogive_nogift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='giftUrl',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]