"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.urls import include
from django.conf.urls.static import static

# Admin customization.
admin.site.site_header = 'Cosmun dashboard'
admin.site.site_title = 'Cosmun dashboard'
admin.site.index_title = 'Administração'


urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/v1/', include('dashboard.api.v1.urls', namespace='api-v1')),

    # Home
    path('', include('dashboard.core.urls', namespace='core')),
]

if settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
