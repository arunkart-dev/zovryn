from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import LoginSerializer, UserSerializer
from apps.roles.permissions import IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['login', 'create']:
            # Login and registration are public
            return [AllowAny()]
        if self.action in ['me']:
            # Any authenticated user can view their own profile
            return [IsAuthenticated()]
        # List, retrieve, update, destroy — admin only
        return [IsAdminUser()]

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        POST /users/login/
        Body: { "username": "...", "password": "..." }
        Returns: { "access": "...", "refresh": "...", "role": "...", "username": "..." }
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user   = serializer.validated_data['user']
        tokens = serializer.get_tokens(user)
        return Response({
            **tokens,
            'role':     user.role,
            'username': user.username,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """
        GET /users/me/
        Returns the currently authenticated user's profile.
        """
        return Response(UserSerializer(request.user).data)