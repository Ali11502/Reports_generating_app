# we need to ensure that whenever a user is created in User, its profile is automatically created. So, we will be using
#  a solution based on django-signals. for this purpose this file is created. user will send signal to profile that user is created so
#  based on that craete a prfile for that user. 
from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print(sender)
    print(instance)
    print(created)
    if created:
        Profile.objects.create(user=instance)