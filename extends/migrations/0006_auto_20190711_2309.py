# Generated by Django 2.0.6 on 2019-07-11 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extends', '0005_auto_20190709_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='username',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='message',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]
