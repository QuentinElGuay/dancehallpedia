# Generated by Django 2.2.5 on 2019-10-30 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dance', '0009_auto_20191010_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeStepName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, max_length=100)),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dance.Step')),
            ],
        ),
    ]
