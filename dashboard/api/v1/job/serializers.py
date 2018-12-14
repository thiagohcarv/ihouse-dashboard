from rest_framework import serializers

from dashboard.job import models
from dashboard.api.v1.base64imagefield import Base64ImageField
from dashboard.api.v1.account import serializers as serializers_account


class ServiceSerializerRetrieve(serializers.ModelSerializer):

    class Meta:
        model = models.Service
        fields = ['id', 'name', 'price']


class CategorySerializerRetrieve(serializers.ModelSerializer):

    thumb = Base64ImageField(represent_in_base64=True)
    services = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ['id', 'thumb', 'name', 'services', 'price']

    def get_services(self, obj):
        return ServiceSerializerRetrieve(obj.services.all(), many=True).data

    def get_price(self, obj):
        return sum([service.price for service in obj.services.all()])


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Job
        fields = ['client', 'services', 'datetime', 'coupon', 'price', 'payed']


class JobAcceptedSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Job
        fields = ['functionary']


class JobStartSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Job
        fields = ['start_datetime']


class JobFinishSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Job
        fields = ['end_datetime']


class JobSerializerRetrieve(serializers.ModelSerializer):

    services = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    client = serializers_account.ClientSerializerRetrieve()
    functionary = serializers_account.FunctionarySerializerRetrieve()

    class Meta:
        model = models.Job
        fields = ['id', 'category', 'client', 'functionary', 'services', 'datetime', 'start_datetime', 'end_datetime', 'price',
                  'coupon', 'payed']

    def get_services(self, obj):
        return ServiceSerializerRetrieve(obj.services.all(), many=True).data

    def get_category(self, obj):
        return CategorySerializerRetrieve(obj.services.first().category).data


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = ['from_user', 'to_user', 'job', 'title', 'content', 'datetime_visualized']


class MessageSerializerRetrieve(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = ['id', 'title', 'content', 'created_at']