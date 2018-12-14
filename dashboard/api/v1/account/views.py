from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from dashboard.account import models
from dashboard.api.v1.account.serializers import UserSerializer, LoginSerializer, ClientSerializer, FunctionarySerializer


class UserViewSet(viewsets.ViewSet):

    serializer_class_user = UserSerializer
    serializer_class_login = LoginSerializer
    serializer_class_client = ClientSerializer
    serializer_class_functionary = FunctionarySerializer

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

    def update(self, request, pk):
        if request.data.get('cpf'):
            functionary = get_object_or_404(models.Functionary, pk=pk)
            serializer = self.serializer_class_functionary(instance=functionary, data=request.data)
        else:
            client = get_object_or_404(models.Client, pk=pk)
            serializer = self.serializer_class_client(instance=client, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({}, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
