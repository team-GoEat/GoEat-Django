# Generated by Django 3.2.6 on 2022-01-13 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_restaurant_res_pos_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rescoupon',
            name='coupon_end_dttm',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='rescoupon',
            name='coupon_start_dttm',
            field=models.DateTimeField(),
        ),
    ]