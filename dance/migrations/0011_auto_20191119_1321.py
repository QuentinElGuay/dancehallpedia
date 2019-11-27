# Generated by Django 2.2.5 on 2019-11-19 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dance', '0010_alternativestepname'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeArtistName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='step',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='stepappearance',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='stepappearance',
            constraint=models.UniqueConstraint(fields=('video', 'step', 'time'), name='step uniqueness'),
        ),
        migrations.AddField(
            model_name='alternativeartistname',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dance.Artist'),
        ),
    ]
