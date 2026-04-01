from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer 
from .permissions import IsSelf, IsSelfOfProvider


# Create your views here.
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            return Response(
                {'error': 'Invalid Credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'email': user.email,
            'id': user.id
        })
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response(
            {'message': 'Logged Out'},
            status=status.HTTP_200_OK
        )


class UserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(
            Q(id=user.id) |
            Q(user_type='P')
        )

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsSelfOfProvider()]
        return [IsAuthenticated(), IsSelf()]