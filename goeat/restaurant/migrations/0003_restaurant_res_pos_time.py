# Generated by Django 3.2.6 on 2021-12-29 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_menu_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='res_pos_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]