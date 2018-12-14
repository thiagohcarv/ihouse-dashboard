from auditlog.registry import auditlog

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from dashboard.storage import get_storage_path
from dashboard.core.models import AbstractBaseModel

User = get_user_model()


def get_category_image_path(instance, filename):
    return get_storage_path(filename, "category")


def get_job_image_path(instance, filename):
    return get_storage_path(filename, "job")


class Category(AbstractBaseModel):

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    thumb = models.ImageField(upload_to=get_category_image_path, verbose_name="Imagem")
    name = models.CharField(verbose_name="Nome", max_length=255)

    def __str__(self):
        return self.name


class Service(AbstractBaseModel):

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    category = models.ForeignKey(Category, verbose_name="Categoria", on_delete=models.CASCADE,
                                 related_name="services")
    name = models.CharField(verbose_name="Nome", max_length=255)
    price = models.DecimalField(verbose_name="Preço", max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name


class Coupon(AbstractBaseModel):

    class Meta:
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"

    title = models.CharField('Titulo', max_length=255)
    code = models.CharField(verbose_name="Código", max_length=120, unique=True)
    quantity = models.PositiveSmallIntegerField(verbose_name='Quantidade', default=1,
                                                validators=[MinValueValidator(1)])
    quantity_used = models.PositiveSmallIntegerField(verbose_name='Quantidade Utilizada', default=0, null=True,
                                                     blank=True)
    price = models.DecimalField(verbose_name="Preço", max_digits=15, decimal_places=2)
    start_date = models.DateTimeField(verbose_name='Válido de')
    end_date = models.DateTimeField(verbose_name='Válido até')
    is_active = models.BooleanField(verbose_name='Está ativo?', default=True)

    def __str__(self):
        return self.title


class Job(AbstractBaseModel):

    class Meta:
        verbose_name = "Trabalho"
        verbose_name_plural = "Trabalhos"

    client = models.ForeignKey('account.Client', verbose_name="Cliente", on_delete=models.CASCADE,
                               related_name="jobs")
    functionary = models.ForeignKey('account.Functionary', verbose_name="Funcionário", on_delete=models.CASCADE,
                               related_name="jobs", null=True, blank=True)

    services = models.ManyToManyField(Service, verbose_name="Trabalho", related_name="jobs")

    datetime = models.DateTimeField(verbose_name="Data/Hora")
    start_datetime = models.DateTimeField(verbose_name="Data/Hora de Inicio", null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name="Data/Hora de Finalização", null=True, blank=True)
    price = models.DecimalField(verbose_name="Preço", max_digits=15, decimal_places=2)
    coupon = models.ForeignKey(Coupon, verbose_name="Cupom", on_delete=models.CASCADE, related_name="jobs",
                               null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude", max_length=255, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude", max_length=255, null=True, blank=True)
    payed = models.BooleanField(verbose_name="Pago?", default=False)

    def __str__(self):
        return str(self.pk)


class JobImage(AbstractBaseModel):

    class Meta:
        verbose_name = "Imagem do Trabalho"
        verbose_name_plural = "Imagens do Trabalho"

    job = models.ForeignKey(Job, verbose_name="Trabalho", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=get_job_image_path, verbose_name="Imagem")

    def __str__(self):
        return str(self.pk)


class Message(AbstractBaseModel):

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'

    from_user = models.ForeignKey(User, verbose_name='De', on_delete=models.CASCADE, related_name='from_messages')
    to_user = models.ForeignKey(User, verbose_name='Para', on_delete=models.CASCADE, related_name='to_messages')
    job = models.ForeignKey('job.Job', verbose_name='Trabalho', on_delete=models.CASCADE, related_name='messages')

    title = models.TextField(verbose_name='Titulo')
    content = models.TextField(verbose_name='Conteudo')
    datetime_visualized = models.DateTimeField(verbose_name="Data/Hora da Visualização", null=True, blank=True)

    def __str__(self):
        return self.title


auditlog.register(Job)
auditlog.register(Coupon)
auditlog.register(Message)
auditlog.register(Service)
auditlog.register(Category)
auditlog.register(JobImage)