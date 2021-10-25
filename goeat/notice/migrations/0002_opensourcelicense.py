# Generated by Django 3.2.3 on 2021-10-05 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenSourceLicense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_title', models.CharField(default='license_title', max_length=30)),
                ('notice_content', models.TextField(blank=True, null=True)),
            ],
        ),
    ]