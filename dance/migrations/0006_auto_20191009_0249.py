# Generated by Django 2.2.5 on 2019-10-09 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dance', '0005_auto_20191009_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='channel',
            field=models.CharField(max_length=30),
        ),
    ]