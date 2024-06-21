from django.contrib.auth import login as auth_login, logout
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializers import UserLoginSerializer, VerifyCodeSerializer, UserSerializer
from .utils import send_verification_code_email, send_verification_code_sms


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# class UserLoginViewSet(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             login = serializer.validated_data.get('login')
#             username = serializer.validated_data.get('username', None)
#             if '@' in login:
#                 user, _ = User.objects.get_or_create(email=login, defaults={'username': username})
#                 code = user.generate_verification_code()
#                 send_verification_code_email(login, code)
#             else:
#                 user, _ = User.objects.get_or_create(phone=login, defaults={'username': username})
#                 code = user.generate_verification_code()
#                 send_verification_code_sms(login, code)

#             return Response({'detail': 'Verification code sent'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data.get('login')
            username = serializer.validated_data.get('username', None)

            if username:  # создание нового пользователя
                if '@' in login:
                    user, created = User.objects.get_or_create(email=login, defaults={'username': username})
                    if created:
                        code = user.generate_verification_code()
                        send_verification_code_email(login, code)
                else:
                    user, created = User.objects.get_or_create(phone=login, defaults={'username': username})
                    if created:
                        code = user.generate_verification_code()
                        send_verification_code_sms(login, code)
                if created:
                    return Response({'detail': 'Verification code sent for new user'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'User already exists, please login'}, status=status.HTTP_400_BAD_REQUEST)
            else:  # логирование существующего
                user = None
                if '@' in login:
                    user = User.objects.filter(email=login).first()
                else:
                    user = User.objects.filter(phone=login).first()

                if user:
                    code = user.generate_verification_code()
                    if '@' in login:
                        send_verification_code_email(login, code)
                    else:
                        send_verification_code_sms(login, code)
                    return Response({'detail': 'Verification code sent'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'User not found, please register'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            user = User.objects.filter(verification_code=code).first()
            
            if user and user.code_expiry > timezone.now():
                user.verification_code = None
                user.code_expiry = None
                user.save()
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                tokens = get_tokens_for_user(user)
                return Response({'detail': 'Login successful', 'tokens': tokens}, status=status.HTTP_200_OK)
            
            return Response({'detail': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get(self, request):
        # print(f"User: {request.user}")  # Отладочная информация
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UserUpdateViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def post(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
