# Generated by Django 3.2.6 on 2022-01-20 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_rescouponlog_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rescouponlog',
            name='res_coupon',
        ),
    ]