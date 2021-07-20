from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *


# @receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
      user = instance
      profile = Profile.objects.create(
          user=user,
          username=user.username,
          email=user.email,
          name=user.first_name,
      )
    print('Profile created!')


def update_user(sender, instance, created, **kwargs):
  profile= instance 
  user = profile.user

  if created == False:
    user.first_name = profile.name
    user.username = profile.username
    user.email = profile.email
    user.save()


  
def delete_user(sender, instance, **kwargs):
  user = instance.user
  user.delete()
  print('Deleting user..')


post_save.connect(create_profile, sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender=Profile)

# print('profile saved!')
# print('Instance:', instance)
# print('CREATED:', created)