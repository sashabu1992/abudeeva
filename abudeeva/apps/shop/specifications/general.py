from django.db import models

class Size(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='Код размера')
    name = models.CharField(max_length=50, verbose_name='Название размера')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return f"{self.name} ({self.code})"


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название цвета')
    code = models.CharField(max_length=7, verbose_name='Код цвета (HEX)', help_text='Например, #FF0000 для красного')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return f"{self.name} ({self.code})"