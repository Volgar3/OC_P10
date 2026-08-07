from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["url", "username", "email", "password", "age", "can_be_contacted", "can_data_be_shared", "is_staff"]
        read_only_fields = ["is_staff"]

    def validate_age(self, value):
        if value < User.MINIMUM_AGE:
            raise serializers.ValidationError(
                f"L'utilisateur doit avoir au moins {User.MINIMUM_AGE} ans."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
