# Generated by Django 4.1.3 on 2022-11-27 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproflie',
            name='coin',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
