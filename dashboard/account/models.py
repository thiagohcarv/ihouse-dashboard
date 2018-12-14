from auditlog.registry import auditlog

from django.db import models
from django.contrib.auth import get_user_model

from dashboard.storage import get_storage_path
from dashboard.core.models import AbstractBaseModel
from dashboard.job.models import Category


User = get_user_model()

def get_user_image_path(instance, filename):
    return get_storage_path(filename, 'user')


class AbstractUserModel(AbstractBaseModel):

    class Meta:
        abstract = True

    thumb = models.ImageField(upload_to=get_user_image_path, verbose_name='Imagem', null=True, blank=True)

    phone = models.CharField(verbose_name='Telefone', max_length=11)
    address = models.CharField(verbose_name='Endereço', max_length=255)
    cpf = models.CharField(verbose_name='CPF', max_length=255, null=True, blank=True)


class Client(AbstractUserModel):

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    user = models.OneToOneField(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='client')

    def __str__(self):
        return self.user.get_full_name() or self.user.first_name or self.user.username


class Functionary(AbstractUserModel):

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    user = models.OneToOneField(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='functionary')
    skills = models.ManyToManyField(Category, verbose_name='Trabalhos', related_name='clients', blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.first_name or self.user.username


auditlog.register(Client)
auditlog.register(Functionary)