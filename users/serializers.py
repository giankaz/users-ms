
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from datetime import date


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField()


class UsersSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)

    def get_age(self, user):
        today = date.today()
        birthdate = user.birthdate
        age = today.year - birthdate.year - \
            ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'age', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data.get('is_superuser'):
            if validated_data.get('password') != '91300962':
                raise ValidationError({'detail': 'You cant do that'})

        user = User.objects.create_user(**validated_data)
        return user
