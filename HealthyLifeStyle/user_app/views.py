from django.contrib.auth import login as auth_login, logout
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import User
from .serializers import UserLoginRegisterSerializer, VerifyCodeSerializer, UserSerializer
from .utils import send_verification_code_email, send_verification_code_sms


class UserRegisterViewSet(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserLoginRegisterSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data.get('login')
            if '@' in login:
                user = User.objects.create(email=login)
                code = user.generate_verification_code()
                send_verification_code_email(login, code)
            else:
                user = User.objects.create(phone=login)
                code = user.generate_verification_code()
                send_verification_code_sms(login, code)
            
            return Response({'detail': 'Verification code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserLoginRegisterSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data.get('login')
            if '@' in login:
                user = User.objects.filter(email=login).first()
                if user:
                    code = user.generate_verification_code()
                    send_verification_code_email(login, code)
            else:
                user = User.objects.filter(phone=login).first()
                if user:
                    code = user.generate_verification_code()
                    send_verification_code_sms(login, code)
            
            return Response({'detail': 'Verification code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeViewSet(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data.get('login')
            code = serializer.validated_data.get('code')
            
            if '@' in login:
                user = User.objects.filter(email=login, verification_code=code).first()
            else:
                user = User.objects.filter(phone=login, verification_code=code).first()
            
            if user and user.code_expiry > timezone.now():
                user.verification_code = None
                user.code_expiry = None
                user.save()
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
            
            return Response({'detail': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutViewSet(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UserUpdateViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
