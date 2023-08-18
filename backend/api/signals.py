from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import *


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)
        print("Created user profile")


@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):

    try:
        if created == False:
            instance.userprofile.save()
            print('Profile updated successfully')

    except:
        instance.userprofile = None


@receiver(post_save, sender=Instructor)
def create_instructor_profile(sender, instance, created, **kwargs):

    if created:
        InstructorProfile.objects.create(user=instance)
        print("Created user profile")


@receiver(post_save, sender=Instructor)
def update_instructor_profile(sender, instance, created, **kwargs):

    try:
        if created == False:
            instance.instructorprofile.save()
            print('Profile updated successfully')

    except:
        instance.instructorprofile = None
