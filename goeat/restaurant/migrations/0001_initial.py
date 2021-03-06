# Generated by Django 3.2.6 on 2021-12-22 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=100)),
                ('menu_image', models.TextField(blank=True, null=True)),
                ('menu_price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MenuCannotEat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cannoteat_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MenuFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MenuFirstClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_class_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MenuIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ing_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MenuType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ResNotice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_title', models.CharField(max_length=255)),
                ('notice_content', models.TextField()),
                ('state', models.BooleanField(default=True)),
                ('notice_create_dttm', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_id', models.CharField(blank=True, max_length=30)),
                ('res_name', models.CharField(max_length=30)),
                ('res_search_name', models.CharField(default='', max_length=30)),
                ('is_affiliate', models.BooleanField(default=False)),
                ('is_reservable_r', models.BooleanField(default=False)),
                ('res_telenum', models.CharField(blank=True, max_length=30)),
                ('res_address', models.CharField(blank=True, max_length=100)),
                ('x_cor', models.CharField(blank=True, default='', max_length=30)),
                ('y_cor', models.CharField(blank=True, default='', max_length=30)),
                ('res_time', models.CharField(blank=True, max_length=100)),
                ('res_exp', models.TextField(blank=True, null=True)),
                ('res_image', models.TextField(blank=True, null=True)),
                ('res_pos_id', models.CharField(blank=True, max_length=100)),
                ('res_pos_pw', models.CharField(blank=True, max_length=100)),
                ('res_open_tm', models.TimeField(blank=True, default='00:00')),
                ('res_close_tm', models.TimeField(blank=True, default='00:00')),
                ('is_breaktime', models.BooleanField(default=False)),
                ('res_break_start_tm', models.TimeField(blank=True, default='00:00')),
                ('res_break_end_tm', models.TimeField(blank=True, default='00:00')),
                ('res_open_days', models.JSONField(default={'week_0': {'name': '?????????', 'state': False}, 'week_1': {'name': '?????????', 'state': False}, 'week_2': {'name': '?????????', 'state': False}, 'week_3': {'name': '?????????', 'state': False}, 'week_4': {'name': '?????????', 'state': False}, 'week_5': {'name': '?????????', 'state': False}, 'week_6': {'name': '?????????', 'state': False}})),
                ('res_menu', models.ManyToManyField(blank=True, related_name='restaurant', to='restaurant.Menu')),
                ('res_type', models.ManyToManyField(blank=True, related_name='restaurant', to='restaurant.MenuType')),
            ],
        ),
        migrations.CreateModel(
            name='ResCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_type', models.BooleanField(default=True)),
                ('coupon_content', models.CharField(max_length=30)),
                ('coupon_count', models.IntegerField(default=0)),
                ('coupon_start_dttm', models.DateTimeField(auto_now_add=True)),
                ('coupon_end_dttm', models.DateTimeField(auto_now_add=True)),
                ('coupon_create_dttm', models.DateTimeField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='MenuSecondClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second_class_name', models.CharField(max_length=30)),
                ('second_class_search_name', models.CharField(max_length=30)),
                ('menu_soup', models.IntegerField(default=0)),
                ('is_spicy', models.BooleanField(default=False)),
                ('is_cold', models.BooleanField(default=False)),
                ('is_favor', models.BooleanField(default=False)),
                ('menu_second_image', models.TextField(blank=True, null=True)),
                ('menu_cannoteat', models.ManyToManyField(blank=True, related_name='menu', to='restaurant.MenuCannotEat')),
                ('menu_feature', models.ManyToManyField(blank=True, related_name='menu', to='restaurant.MenuFeature')),
                ('menu_first_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='menu', to='restaurant.menufirstclass')),
                ('menu_ingredients', models.ManyToManyField(blank=True, related_name='menu', to='restaurant.MenuIngredient')),
                ('menu_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='menu', to='restaurant.menutype')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_second_name',
            field=models.ManyToManyField(blank=True, related_name='menu', to='restaurant.MenuSecondClass'),
        ),
    ]
