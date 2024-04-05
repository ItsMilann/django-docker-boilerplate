from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True, required=True)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "fullname",
            "image_url",
            "email",
            "phone",
            "password",
            "profile",
            "token",
            "role",
        ]
        extra_kwargs = {
            "token": {"write_only": True},
            "role": {"write_only": True},
        }

    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        password = validated_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = validated_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return instance


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        assert isinstance(self.user, models.User)
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["phone"] = self.user.phone
        data["role"] = self.user.role
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
