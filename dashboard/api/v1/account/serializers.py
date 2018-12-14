from base64 import b64encode

from itsdangerous import TimedJSONWebSignatureSerializer
from rest_framework import serializers

from django.conf import settings
from django.contrib.auth import get_user_model

from dashboard.account import models
from dashboard.api.v1.base64imagefield import ImageSerializer

User = get_user_model()


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        try:
            self.functionary = None
            self.user = models.Client.objects.filter(user__email=data.get('email'))
            if not self.user.exists():
                self.user = models.Functionary.objects.filter(user__email=data.get('email'))
                if self.user.exists():
                    self.functionary = self.user.first().pk

            if self.user.exists():
                self.user = self.user.first()
            else:
                raise serializers.ValidationError('Email or password does not match.', code='invalid')

            if not self.user.user.check_password(data.get('password')):
                raise serializers.ValidationError('Email or password does not match.', code='invalid')
        except models.Client.DoesNotExist:
            raise serializers.ValidationError('Email or password does not match.', code='invalid')

        return data

    def get_data(self):
        data = {
            'token': self.get_token(),
            'user': {
                'functionary': self.functionary,
                'thumb': ImageSerializer(self.user.thumb).data if self.user.thumb else None,
                'name': self.user.user.get_full_name() or self.user.user.username
            }
        }
        return data

    def get_token(self):
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=settings.EXPIRES_IN)
        token = serializer.dumps({'username': self.validated_data['email'],
                                  'password': self.validated_data['password']})

        return b64encode(token)


class UserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def validate(self, data):
        if not self.instance and User.objects.filter(username=data.get('email')).exists():
            raise serializers.ValidationError('This email already exists!', code='invalid')
        elif self.instance and User.objects.filter(username=data.get('email')).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('This email already exists!', code='invalid')

        return data

    def create(self, validated_data):
        user = User(
            first_name=validated_data['name'],
            email=validated_data['email'],
            username=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('email', instance.email)
        instance.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Client
        fields = ['user', 'address', 'phone']


class ClientSerializerRetrieve(serializers.ModelSerializer):

    thumb = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = models.Client
        fields = ['name', 'email', 'thumb', 'address', 'phone']

    def get_thumb(self, obj):
        return ImageSerializer(obj.thumb).data if obj.thumb else None

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_email(self, obj):
        return obj.user.email


class FunctionarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Functionary
        fields = ['user', 'address', 'phone', 'cpf']


class FunctionarySerializerRetrieve(serializers.ModelSerializer):

    thumb = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = models.Functionary
        fields = ['name', 'email', 'thumb', 'address', 'phone', 'cpf']

    def get_thumb(self, obj):
        return ImageSerializer(obj.thumb).data if obj.thumb else None

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_email(self, obj):
        return obj.user.email
