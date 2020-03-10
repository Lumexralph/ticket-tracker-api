# Generated by Django 3.0.4 on 2020-03-10 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200310_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='role',
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(null=True, related_name='roles', to='account.Permission'),
        ),
    ]
