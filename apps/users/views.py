from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        role = serializer.validated_data.get('role', '').upper()

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'detail': "Login yoki parol noto'g'ri!"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'detail': 'Foydalanuvchi bloklangan!'}, status=status.HTTP_403_FORBIDDEN)

        if role and user.role != role:
            return Response({'detail': f"Bu foydalanuvchi {role} roliga ega emas!"}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
            }
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refreshToken') or request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass
        return Response({'success': True})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'success': True, 'data': UserSerializer(request.user).data})

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'data': serializer.data})


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token kerak!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            return Response({'access': str(refresh.access_token)})
        except TokenError:
            return Response({'detail': 'Token yaroqsiz!'}, status=status.HTTP_401_UNAUTHORIZED)
