from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_reciever(sender, instance, created, **kwargs):
    
    if created:
        UserProfile.objects.create(user=instance)
        print('User profile is created')
        #Create Profile
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
           
        except:
            #create profile if not exist
            UserProfile.objects.create(user=instance)
        
# post_save.connect(post_save_create_reciever, sender=User)

@receiver(pre_save, sender=User)
def pre_save_profile_reciever(sender,instance,**kwargs):
    pass