from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from users.permissions import ListCreatePermission, LoginPermission, GeneralPermission

from .models import User
from .serializers import LoginSerializer, UsersSerializer
# Create your views here.


class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [GeneralPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_destroy(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, serializer):
        serializer.save(is_active=False)


class ListCreateUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [GeneralPermission]


class ReactivateView(APIView):
    queryset = User
    serializer_class = LoginSerializer

    def patch(self, request, user_id):
        instance = User.objects.get(pk=user_id)
        serializer = UsersSerializer(instance, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    queryset = User
    serializer_class = LoginSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [LoginPermission]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]

        user = authenticate(
            username=username,
            password=serializer.validated_data["password"]
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            if user.is_active == False:
                return Response({'detail': 'User is inactive', 'token': token.key})

            return Response({'token': token.key})

        return Response(
            {'detail': 'Invalid username or password'},
            status.HTTP_400_BAD_REQUEST
        )
