from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class BlazersAttributes(models.Model):
    # характеристики для жакетов и пиджаков
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Характеристики
    size = models.CharField(max_length=50, verbose_name='Размер', blank=True)
    fason = models.CharField(max_length=50, verbose_name='Фосан', blank=True)

    class Meta:
        verbose_name = 'Характеристики жакета'
        verbose_name_plural = 'Характеристики жакетов'

    def __str__(self):
        return f"Жакет: {self.size}, {self.fason}"