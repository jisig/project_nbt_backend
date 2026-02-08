
import profile
from array import array

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "otp_required": True,
                    "message": "OTP sent",
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializers import OTPVerifySerializer

class   OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.save()
            return Response(
                {
                    "message": "OTP verified",
                    "tokens": tokens
                }
            )
        return Response(serializer.errors, status=400)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer
#
class CreateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if Profile.objects.filter(user=user).exists():
            return Response(
                {"detail": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfileSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        profile = serializer.save(user=user)

        return Response(
            ProfileSerializer(profile).data,
            status=status.HTTP_201_CREATED
        )

from django.contrib.auth import authenticate

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTP

class LoginView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile_number")
        password = request.data.get("password")

        if not mobile or not password:
            return Response(
                {"error": "Mobile number and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=mobile, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.is_active:
            return Response(
                {"error": "Account inactive"},
                status=status.HTTP_403_FORBIDDEN
            )

        otp = "0089"

        OTP.objects.update_or_create(
            user=user,
            defaults={"otp": otp, "is_verified": False}
        )

        return Response(
            {
                "otp_required": True,
                "message": "OTP sent"
            },
            status=status.HTTP_200_OK
        )


from rest_framework_simplejwt.tokens import RefreshToken

class LoginOTPVerifyView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile_number")
        otp = request.data.get("otp")

        if not mobile or not otp:
            return Response(
                {"error": "mobile_number and otp are required"},
                status=400
            )

        try:
            user = User.objects.get(username=mobile)
            otp_obj = OTP.objects.get(user=user, otp=otp, is_verified=False)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except OTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=400)

        otp_obj.is_verified = True
        otp_obj.save()

        refresh = RefreshToken.for_user(user)

        try:
            profile = Profile.objects.get(user=user)
            profile_data = ProfileSerializer(profile).data
        except Profile.DoesNotExist:
            profile_data = None

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "profile": profile_data
        }, status=200)

# api/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class SearchUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("username")

        if not username:
            return Response({"error": "username is required"}, status=400)

        qs = Profile.objects.filter(
            username__icontains=username,
            is_active_profile=True
        )

        serializer = ProfileSerializer(qs, many=True)
        return Response(serializer.data, status=200)

