# Generated by Django 2.2.5 on 2019-10-10 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dance', '0008_auto_20191009_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='step',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(db_index=True),
        ),
    ]