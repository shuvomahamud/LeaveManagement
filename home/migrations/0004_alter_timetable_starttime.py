# Generated by Django 4.0.3 on 2022-03-30 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_timetable_endtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='startTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]