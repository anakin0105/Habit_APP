
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

# Create your views here.
from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()