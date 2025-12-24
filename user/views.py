from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exeption=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"user": serializer.data, "token": token.key}, status=201, headers=headers
        )
