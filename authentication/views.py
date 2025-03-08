from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "password"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data.get("phone_number"),
            password=validated_data.get("password"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class RegisterApiView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": RegisterSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
