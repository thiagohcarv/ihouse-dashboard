from django.contrib import admin

from dashboard.account import models
from dashboard.core.admin import thumbnail


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):

    fields = ['user', 'thumb', 'phone', 'address', 'cpf']
    list_display = ['id', 'thumbnail', 'user_name', 'created_at', 'updated_at']
    list_display_links = ['id', 'thumbnail', 'user_name']

    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.first_name or obj.user.username
    user_name.short_description = 'Usuário'

    def thumbnail(self, obj):
        return thumbnail(obj.thumb)
    thumbnail.short_description = 'Imagem'


@admin.register(models.Functionary)
class FunctionaryAdmin(admin.ModelAdmin):

    fields = ['user', 'thumb', 'phone', 'address', 'cpf', 'skills']
    list_display = ['id', 'thumbnail', 'user', 'skills', 'created_at', 'updated_at']
    list_display_links = ['id', 'thumbnail', 'user']

    def thumbnail(self, obj):
        return thumbnail(obj.thumb)
    thumbnail.short_description = 'Imagem'

    def skills(self, obj):
        html = ''
        for skill in obj.skills.all():
            html += '<div>'+skill.name+'</div>'
        return mark_safe(html)
    skills.short_description = 'Trabalhos'