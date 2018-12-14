from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from dashboard.account import models
from dashboard.api.v1.account import serializers


class UserViewSet(viewsets.ViewSet):

    serializer_class_user = serializers.UserSerializer
    serializer_class_login = serializers.LoginSerializer
    serializer_class_client = serializers.ClientSerializer
    serializer_class_functionary = serializers.FunctionarySerializer
    serializer_class_client_retrieve = serializers.ClientSerializerRetrieve
    serializer_class_functionary_retrieve = serializers.FunctionarySerializerRetrieve

    def login(self, request):
        serializer = self.serializer_class_login(data=request.data)

        if serializer.is_valid():
            return Response(serializer.get_data(), status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        serializer_user = self.serializer_class_user(data=request.data)

        if serializer_user.is_valid():
            user = serializer_user.save()
            data = request.data.copy()
            data['user'] = user.pk
            if request.data.get('cpf'):
                serializer = self.serializer_class_functionary(data=data)
            else:
                serializer = self.serializer_class_client(data=data)

            if serializer.is_valid():
                serializer.save()

                # LOGIN
                serializer = self.serializer_class_login(data=request.data)
                if serializer.is_valid():
                    return Response(serializer.get_data(), status=status.HTTP_200_OK)

                return Response({}, status=status.HTTP_200_OK)
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': serializer_user.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        serializer_user = self.serializer_class_user(instance=request.user, data=request.data, partial=True)

        if serializer_user.is_valid():
            user = serializer_user.save()
            data = request.data.copy()
            data.update({'user': user.pk})

            if hasattr(request.user, 'functionary'):
                serializer = self.serializer_class_functionary(instance=request.user.functionary, data=data)
            else:
                serializer = self.serializer_class_client(instance=request.user.client, data=data)
            if serializer.is_valid():
                serializer.save()

                return Response({}, status=status.HTTP_200_OK)
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': serializer_user.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if hasattr(request.user, 'functionary'):
            user = models.Functionary.objects.get(pk=request.user.functionary.pk)
            context = self.serializer_class_functionary_retrieve(user).data
        else:
            user = models.Client.objects.get(pk=request.user.client.pk)
            context = self.serializer_class_client_retrieve(user).data

        return Response(context, status=status.HTTP_200_OK)
