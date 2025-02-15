from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .general import Color,Size



class DressesAttributes(models.Model):
    # характеристики для платья
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Характеристики
    colors = models.ManyToManyField(Color, blank=True, verbose_name='Цвет')
    sizes = models.ManyToManyField(Size, verbose_name='Размер', blank=True)
    fason = models.CharField(max_length=100, verbose_name='Фасон', blank=True)

    class Meta:
        verbose_name = 'Характеристики платья'
        verbose_name_plural = 'Характеристики платьев'

    def __str__(self):
        return f"Платье: {self.colors.name}, {self.sizes}, {self.fason}"

