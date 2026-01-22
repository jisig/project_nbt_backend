# from django.db import models
#
# # Create your models here.

from django.db import models
from django.contrib.auth.models import User

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    display_name = models.CharField(max_length=100)
    interest = models.CharField(max_length=100)
    pronouns = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    city = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    username = models.CharField(
        max_length=30,
        unique=True
    )

    display_name = models.CharField(max_length=100)
    vibe = models.CharField(max_length=100)
    pronouns = models.CharField(max_length=20)
    dob = models.DateField()
    city = models.CharField(max_length=100)

    is_active_profile = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username



class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
