# Generated by Django 2.1.4 on 2018-12-12 20:17

import dashboard.account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('thumb', models.ImageField(upload_to=dashboard.account.models.get_user_image_path, verbose_name='Imagem')),
                ('phone', models.CharField(max_length=11, verbose_name='Telefone')),
                ('address', models.CharField(max_length=255, verbose_name='Endereço')),
                ('cpf', models.CharField(blank=True, max_length=255, null=True, verbose_name='CPF')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Functionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('thumb', models.ImageField(upload_to=dashboard.account.models.get_user_image_path, verbose_name='Imagem')),
                ('phone', models.CharField(max_length=11, verbose_name='Telefone')),
                ('address', models.CharField(max_length=255, verbose_name='Endereço')),
                ('cpf', models.CharField(blank=True, max_length=255, null=True, verbose_name='CPF')),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('content', models.TextField(verbose_name='Conteudo')),
                ('visualized', models.BooleanField(default=False, verbose_name='Visualizado?')),
                ('date_visualized', models.DateTimeField(blank=True, null=True, verbose_name='Data/Hora da Visualização')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_messages', to=settings.AUTH_USER_MODEL, verbose_name='De')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_messages', to=settings.AUTH_USER_MODEL, verbose_name='Para')),
            ],
            options={
                'verbose_name': 'Mensagem',
                'verbose_name_plural': 'Mensagens',
            },
        ),
    ]