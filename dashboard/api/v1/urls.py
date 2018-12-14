from django.urls import path
from django.urls import include

from rest_framework import routers

from dashboard.api.v1.account import views as views_account
from dashboard.api.v1.job import views as views_job

app_name = 'api.v1'

router = routers.SimpleRouter()
router.register('job', views_job.JobViewSet, base_name='job')
router.register('message', views_job.MessageViewSet, base_name='message')

urlpatterns = [
    path('login/', views_account.UserViewSet.as_view({'post': 'login'}), name='login'),
    path('register/', views_account.UserViewSet.as_view({'post': 'register'}), name='register-user'),
    path('register/<int:pk>/', views_account.UserViewSet.as_view({'put': 'update'}), name='update-user'),

    path('category/', views_job.CategoryViewSet.as_view({'get': 'get'}), name='category'),
    path('job/accept/<int:pk>/', views_job.JobViewSet.as_view({'patch': 'accept'}), name='accept-job'),
    path('job/start/<int:pk>/', views_job.JobViewSet.as_view({'patch': 'start'}), name='start-job'),
    path('job/finish/<int:pk>/', views_job.JobViewSet.as_view({'patch': 'finish'}), name='finish-job'),

    path('', include(router.urls)),
]
