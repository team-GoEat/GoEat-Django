# Generated by Django 3.2.3 on 2021-12-08 10:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_team_menu_cannoteat'),
    ]

    operations = [
        migrations.AddField(
            model_name='resreservationrequest',
            name='res_deadline_time',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
            preserve_default=False,
        ),
    ]
