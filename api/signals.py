# api/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Profile

@receiver(pre_save, sender=Profile)
def handle_profile_disable(sender, instance, **kwargs):
    if not instance.pk:
        return  # new profile, ignore

    old = Profile.objects.get(pk=instance.pk)

    # if admin turns OFF the profile
    if old.is_active_profile is True and instance.is_active_profile is False:
        purge_profile_data(instance)


def purge_profile_data(profile):
    # delete ONLY profile-created data

    # example (future-safe):
    # profile.interests.all().delete()
    # profile.posts.all().delete()
    # profile.matches.all().delete()

    profile.delete()
