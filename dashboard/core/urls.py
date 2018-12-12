from django.urls import path

from dashboard.core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
]
