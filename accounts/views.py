from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# ================= Register =================
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User registered successfully"}, status=201)


# ================= Login =================
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })


# ================= Forgot Password =================
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def forgot_password(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is required"}, status=400)

    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"error": "User not found"}, status=404)

    token = PasswordResetTokenGenerator().make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}"

    send_mail(
        "Password Reset",
        f"Click here to reset your password: {reset_link}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    return Response({"message": "Password reset email sent"})


# ================= Reset Password =================
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"error": "Invalid link"}, status=400)

    if not PasswordResetTokenGenerator().check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=400)

    password = request.data.get("password")
    password2 = request.data.get("password2")

    if not password or not password2:
        return Response({"error": "Both password fields are required"}, status=400)
    if password != password2:
        return Response({"error": "Passwords do not match"}, status=400)

    user.set_password(password)
    user.save()
    return Response({"message": "Password has been reset successfully"})
