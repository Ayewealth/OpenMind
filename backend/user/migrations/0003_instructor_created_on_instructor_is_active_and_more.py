# Generated by Django 4.2.3 on 2023-07-10 12:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='instructor',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='instructor',
            name='is_instructor',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='instructor',
            name='updated_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
