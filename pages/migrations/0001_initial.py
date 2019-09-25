# Generated by Django 2.2.5 on 2019-09-24 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('school', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Old school'), (2, 'Middle school'), (3, 'New school')], default=0)),
                ('creator', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('channel', models.CharField(max_length=20)),
                ('channel_url', models.URLField()),
                ('valid', models.BooleanField(default=True)),
                ('host', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Youtube'), (2, 'Instagram')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StepAppearance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(null=True)),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Step')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Video')),
            ],
        ),
        migrations.AddField(
            model_name='step',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='steps', to='pages.Tag'),
        ),
    ]
