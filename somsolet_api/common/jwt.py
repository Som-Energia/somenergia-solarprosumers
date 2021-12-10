from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class SomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.get_username()
        token['name'] = user.get_full_name()
        token['email'] = user.email

        return token

class SomTokenObtainPairView(TokenObtainPairView):
    serializer_class = SomTokenObtainPairSerializer
