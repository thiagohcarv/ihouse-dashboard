from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404

from dashboard.job import models
from dashboard.api.v1.job import serializers


class CategoryViewSet(viewsets.ViewSet):

    serializer_class = serializers.CategorySerializerRetrieve

    def get_queryset(self):
        return models.Category.objects.all()

    def get(self, request):
        return Response(self.serializer_class(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)


class JobViewSet(viewsets.ModelViewSet):

    paginate_by = None
    serializer_class = serializers.JobSerializer
    serializer_class_finished = serializers.JobFinishSerializer
    serializer_class_accepted = serializers.JobAcceptedSerializer
    serializer_class_retrieve = serializers.JobSerializerRetrieve

    def get_queryset(self):
        if self.request.GET.get('category'):
            return models.Job.objects.filter(services__category__id=self.request.GET.get('category'), end_datetime__isnull=True).distinct()
        elif self.request.user.functionary:
            return models.Job.objects.filter(functionary=self.request.user.functionary)
        return models.Job.objects.filter(client=self.request.user.client)

    def list(self, request):
        return Response(self.serializer_class_retrieve(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data.copy()
        data.update({'client': request.user.client.pk})
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            job = serializer.save()

            return Response(self.serializer_class_retrieve(job).data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        raise MethodNotAllowed('PUT')

    def destroy(self, request, pk):
        raise MethodNotAllowed('DELETE')

    def retrieve(self, request, pk):
        job = get_object_or_404(models.Job, pk=pk)
        context = self.serializer_class_retrieve(job).data
        context['is_accept'] = False
        if job.functionary:
            context['is_accept'] = job.functionary.pk == request.user.functionary.pk
        return Response(context, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        raise MethodNotAllowed('PATCH')

    def accept(self, request, pk):
        job = get_object_or_404(models.Job, pk=pk)
        serializer = self.serializer_class_accepted(instance=job, data={'functionary': request.user.functionary.pk})

        if serializer.is_valid():
            serializer.save()

            return Response({}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def start(self, request, pk):
        job = get_object_or_404(models.Job, pk=pk, functionary=request.user.functionary)
        serializer = self.serializer_class_accepted(instance=job, data={'start_datetime': timezone.now()})

        if serializer.is_valid():
            job.start_datetime = timezone.now()
            job.save()

            return Response({}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def finish(self, request, pk):
        job = get_object_or_404(models.Job, pk=pk, functionary=request.user.functionary)
        serializer = self.serializer_class_finished(instance=job, data={'end_datetime': timezone.now()})

        if serializer.is_valid():
            job.end_datetime = timezone.now()
            job.save()

            return Response({}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):

    paginate_by = None
    serializer_class = serializers.MessageSerializer
    serializer_class_retrieve = serializers.MessageSerializerRetrieve

    def get_queryset(self):
        if self.request.GET.get('job'):
            return models.Message.objects.filter(job_id=self.request.GET.get('job'))
        return models.Message.objects.filter(Q(from_user=self.request.user) | Q(to_user=self.request.user))

    def list(self, request):
        return Response(self.serializer_class_retrieve(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)

    def create(self, request):
        job = models.Job.objects.get(pk=request.data.get('job'))
        data = request.data.copy()
        if request.user.functionary:
            to_user = job.client.user.pk
            data.update({'from_user': request.user.functionary.user.pk})
        else:
            to_user = job.functionary.user.pk
            data.update({'from_user': request.user.client.user.pk})

        data.update({'job': job.id, 'to_user': to_user})

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            job = serializer.save()

            return Response(self.serializer_class_retrieve(job).data, status=status.HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
