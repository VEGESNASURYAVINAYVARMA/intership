from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import User
from .serializers import UserRegisterSerializer
from .utils import send_sms

# ---------- Helper ----------
def generate_random_password(length=8):
    import string, random
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# -------- STEP 1: REGISTER USER --------
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data.get('phone_number')

            # Create user (auto password)
            user = User.objects.create_user(
                name=name,
                email=email,
                phone_number=phone_number
            )

            # Get plain password (from create_user)
            password = user.password  # user.password is hashed, need plain
            # Since your manager generates random password, we can regenerate to email plain
            plain_password = generate_random_password()
            user.set_password(plain_password)
            user.save()

            # Send registration email
            subject = 'Registration Successful - Hybrid LMS'
            message = (
                f"Hi {user.name},\n\n"
                f"Your User ID: {user.user_id}\n"
                f"Your Temporary Password: {plain_password}\n\n"
                f"Please log in using your user ID and reset your password.\n\n"
                f"Thank you,\nHybrid LMS Team"
            )
            send_mail(subject, message, None, [user.email])

            return Response({
                "message": "Registration successful. Email sent.",
                "user_id": user.user_id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------- STEP 2: PASSWORD RESET (No OTP) --------
class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate new password
        new_password = generate_random_password()
        user.set_password(new_password)
        user.save()

        # Send password via email
        subject = "Password Reset - Hybrid LMS"
        message = (
            f"Hi {user.name},\n\n"
            f"Your new temporary password is: {new_password}\n"
            f"You can log in and then reset it if you wish.\n\n"
            f"Thank you,\nHybrid LMS Team"
        )
        send_mail(subject, message, None, [user.email])

        return Response({"message": "New password sent to your email."}, status=status.HTTP_200_OK)


# -------- STEP 3: LOGIN (SEND OTP) --------
class UserLoginView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        if not all([user_id, password]):
            return Response({"error": "User ID and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, user_id=user_id, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate OTP
        otp = user.generate_otp()

        # Send Email
        subject = 'Hybrid LMS Login OTP'
        message = f"Hi {user.name},\nYour OTP is {otp}. It expires in 5 minutes."
        send_mail(subject, message, None, [user.email])

        # Send SMS
        
        if user.phone_number:
            send_sms(user.phone_number, otp)
    
        return Response({
            'message': f"OTP sent to {user.email} and {user.phone_number if user.phone_number else 'email only'}.", 'sms_result': sms_result
        }, status=status.HTTP_200_OK)


# -------- STEP 4: VERIFY OTP --------
class VerifyOTPView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        otp = request.data.get('otp')
        if not all([user_id, otp]):
            return Response({"error": "User ID and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.verify_otp(otp):
            # Clear OTP
            user.otp_code = None
            user.otp_expiry = None
            user.save()

            # Issue JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'OTP verified successfully. Login successful.',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
