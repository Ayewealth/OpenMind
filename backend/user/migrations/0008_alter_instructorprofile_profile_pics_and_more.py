# Generated by Django 4.2.3 on 2023-07-11 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_instructor_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructorprofile',
            name='profile_pics',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pics',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]
