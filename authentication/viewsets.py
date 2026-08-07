from rest_framework import viewsets
from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.permissions import IsSelfOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated(), IsSelfOrReadOnly()]
