from django.contrib import admin
from django.utils.safestring import mark_safe

from dashboard.job import models
from dashboard.core.admin import thumbnail


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'thumbnail', 'name', 'created_at', 'updated_at']
    list_display_links = ['id', 'thumbnail', 'name']

    def thumbnail(self, obj):
        return thumbnail(obj.thumb)
    thumbnail.short_description = 'Imagem'


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = ['id', 'category', 'name', 'price', 'created_at', 'updated_at']
    list_display_links = ['id', 'category', 'name']


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):

    list_display = ['id', 'services_name', 'client', 'functionary', 'price', 'created_at', 'updated_at']
    list_display_links = ['id', 'services_name']

    def services_name(self, obj):
        html = ''
        for service in obj.services.all():
            html += '<div>'+service.name+'</div>'
        return mark_safe(html)
    services_name.short_description = 'Serviços'


@admin.register(models.Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'code', 'quantity', 'quantity_used', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'title', 'code']