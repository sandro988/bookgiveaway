from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer as DjangoRestAuthLoginSerializer


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "id"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user


class LoginSerializer(DjangoRestAuthLoginSerializer):
    """
    Overriding LoginSerializer from dj_rest_auth package so that
    there is no need for users to input username when they want to sign in.
    """

    username = None
