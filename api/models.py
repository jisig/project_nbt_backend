# from django.db import models
#
# # Create your models here.
import uuid

from django.db import models
from django.contrib.auth.models import User

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=100)
    vibe = models.CharField(max_length=100)
    pronouns = models.CharField(max_length=20)
    dob = models.DateField()
    city = models.CharField(max_length=100)

    is_active_profile = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

