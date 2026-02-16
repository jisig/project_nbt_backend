from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import OTP
from .models import Profile

# class RegisterSerializer(serializers.Serializer):
#     mobile = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#
#     def validate_mobile(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("Account already exists")
#         return value
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data["mobile"],
#             password=validated_data["password"],
#             is_active=False,
#             is_staff=False,
#             is_superuser=False,
#         )
#
#         OTP.objects.create(
#             user=user,
#             otp="0089"  # STATIC OTP FOR DEV ONLY
#         )
#
#         return user
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
            is_active=False,
            is_staff=False,
            is_superuser=False,
        )

        OTP.objects.create(
            user=user,
            otp="0089",   # DEV ONLY
            is_verified=False
        )

        return user

# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import OTP

# class OTPVerifySerializer(serializers.Serializer):
#     mobile = serializers.CharField()
#     otp = serializers.CharField()
#
#     def validate(self, data):
#         try:
#             user = User.objects.get(username=data["mobile"])
#             otp_obj = OTP.objects.get(user=user, otp=data["otp"])
#         except (User.DoesNotExist, OTP.DoesNotExist):
#             raise serializers.ValidationError("Invalid OTP")
#
#         data["user"] = user
#         return data
#
#     def create(self, validated_data):
#         user = validated_data["user"]
#         user.is_active = True
#         user.is_staff = False
#         user.is_superuser = False
#         user.save()
#
#         otp_obj = OTP.objects.get(user=user)
#         otp_obj.is_verified = True
#         otp_obj.save()
#
#         refresh = RefreshToken.for_user(user)
#
#         return {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token)
#         }

class OTPVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        mobile = data.get("mobile")
        otp_value = data.get("otp")

        # 1️⃣ Check user exists
        try:
            user = User.objects.get(username=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError({"mobile": "Invalid user"})

        # 2️⃣ Check OTP generated
        try:
            otp_obj = OTP.objects.get(user=user)
        except OTP.DoesNotExist:
            raise serializers.ValidationError({"otp": "OTP not generated"})

        # 3️⃣ Check if already verified
        if otp_obj.is_verified:
            raise serializers.ValidationError({"otp": "OTP already used"})

        # 4️⃣ Check OTP value
        if otp_obj.otp != otp_value:
            raise serializers.ValidationError({"otp": "Invalid OTP"})

        data["user"] = user
        data["otp_obj"] = otp_obj
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        otp_obj = validated_data["otp_obj"]

        # Activate user
        user.is_active = True
        user.save()

        # Mark OTP verified
        otp_obj.is_verified = True
        otp_obj.save()

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


# from rest_framework import serializers
# from .models import Profile




# from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = (
            "user",
            "username",
            "display_name",
            "vibe",
            "pronouns",
            "dob",
            "city",
            "is_active_profile",
        )

    def validate_username(self, value):
        if Profile.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value
