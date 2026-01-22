from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP
from .models import Profile

class RegisterSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_mobile(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Account already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["mobile"],
            password=validated_data["password"],
            is_active=False
        )

        OTP.objects.create(
            user=user,
            otp="1234"  # STATIC OTP FOR DEV ONLY
        )

        return user

# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import OTP

class OTPVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data["mobile"])
            otp_obj = OTP.objects.get(user=user, otp=data["otp"])
        except (User.DoesNotExist, OTP.DoesNotExist):
            raise serializers.ValidationError("Invalid OTP")

        data["user"] = user
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        user.is_active = True
        user.save()

        otp_obj = OTP.objects.get(user=user)
        otp_obj.is_verified = True
        otp_obj.save()

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

# from rest_framework import serializers
# from .models import Profile

from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "username",
            "display_name",
            "vibe",
            "pronouns",
            "dob",
            "city",
        )


    class LoginSerializer(serializers.Serializer):
        mobile_number = serializers.CharField()
        password = serializers.CharField()

    # def validate(self, attrs):
    #     user = self.context["request"].user
    #
    #     if hasattr(user, "profile"):
    #         raise serializers.ValidationError("Profile already exists")
    #
    #     if not user.is_active:
    #         raise serializers.ValidationError("User is not verified")
    #
    #     return attrs
