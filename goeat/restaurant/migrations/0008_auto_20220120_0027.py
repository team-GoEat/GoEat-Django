# Generated by Django 3.2.6 on 2022-01-20 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_usercoupon_user_coupon_key'),
        ('restaurant', '0007_remove_rescouponlog_res_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rescouponlog',
            name='user',
        ),
        migrations.AddField(
            model_name='rescouponlog',
            name='user_coupon',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='accounts.usercoupon'),
        ),
    ]
