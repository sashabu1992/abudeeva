import os

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from slugify import slugify
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
import uuid


def increment_slug_category(slug, obj):
    """
    Добавляет числовой суффикс к slug, если он уже существует в базе данных.
    Например, если slug="test", а в базе данных уже есть запись с таким slug,
    то функция вернет "test-1". Если "test-1" тоже уже существует, то вернет "test-2" и т.д.
    """
    original_slug = slug
    counter = 1
    while CategoryShop.objects.filter(slug=slug).exclude(id=obj.id).exists():
        slug = '{}-{}'.format(original_slug, counter)
        counter += 1
    return slug if original_slug == slug else slug + '-1'

def get_file_image_cat_zast(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images/category', str(instance.id), 'zast', filename)

class CategoryShop(MPTTModel):
    slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name="URl")
    """СЕО настройки"""
    title = models.CharField(max_length=255, verbose_name="Заголовок Title")
    description = models.CharField(max_length=350, verbose_name="Описание Description", blank=True)
    """Основные данные """
    h1 = models.CharField(max_length=255, verbose_name="Заголовок H1")
    zast = models.ImageField(upload_to=get_file_image_cat_zast, verbose_name="Фото", blank=True, default='defaults/default.png')
    created = models.DateField(auto_now_add=True, blank=True, verbose_name="Дата создания")
    modified = models.DateField(auto_now=True, verbose_name="Дата изменения")
    is_draft = models.BooleanField(default=True, verbose_name="Опубликован")

    # Поле для связи с родительской категорией
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')

    # Поле для выбора типа характеристик
    ATTRIBUTE_CHOICES = [
        ('dresses', 'Цвет-Размер'),
    ]
    attribute_type = models.CharField(
        max_length=50,
        choices=ATTRIBUTE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Тип характеристик'
    )

    class MPTTMeta:
        order_insertion_by = ['h1']

    class Meta:
        ordering = ('title',)
        verbose_name = ('Категория')
        verbose_name_plural = ('Категории')

    def __str__(self):
        """Return title and username."""
        return str(self.h1)

    def get_absolute_url(self):
        return reverse('category_tovar', kwargs={'slug_category': self.slug})  # new

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.title)
        while CategoryShop.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = increment_slug_category(self.slug, self)
        super(CategoryShop, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CategoryShop, self).save(*args, **kwargs)



def increment_slug_tovar(slug, obj):
    """
    Добавляет числовой суффикс к slug, если он уже существует в базе данных.
    Например, если slug="test", а в базе данных уже есть запись с таким slug,
    то функция вернет "test-1". Если "test-1" тоже уже существует, то вернет "test-2" и т.д.
    """
    original_slug = slug
    counter = 1
    while CategoryShop.objects.filter(slug=slug).exclude(id=obj.id).exists():
        slug = '{}-{}'.format(original_slug, counter)
        counter += 1
    return slug if original_slug == slug else slug + '-1'


def get_file_image_zast(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images/tovar', str(instance.id), 'zast', filename)

class TovarShop(models.Model):
    slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name="URl")
    """СЕО настройки"""
    title = models.CharField(max_length=255, verbose_name="Заголовок Title")
    description = models.CharField(max_length=350, verbose_name="Описание Description", blank=True)
    """Основные данные """
    h1 = models.CharField(max_length=255, verbose_name="Заголовок H1")
    zast = models.ImageField(upload_to=get_file_image_zast, verbose_name="Фото", blank=True)
    article = models.CharField(max_length=255, verbose_name="Артикул", blank=True)
    # Новые поля для цены и старой цены
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Цена",default=0.00, blank=True)
    old_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Старая цена", blank=True, null=True)
    is_popular = models.BooleanField(default=False, verbose_name="Популярный")
    is_new = models.BooleanField(default=False, verbose_name="Новый")

    created = models.DateField(auto_now_add=True, blank=True, verbose_name="Дата создания")
    modified = models.DateField(auto_now=True, verbose_name="Дата изменения")
    is_draft = models.BooleanField(default=True, verbose_name="Опубликован")


    # Связь с категорией
    category = models.ForeignKey(
        CategoryShop,
        on_delete=models.PROTECT,  # Запрещаем удаление категории, если с ней связаны товары
        related_name='tovars',
        verbose_name='Категория'
    )

    # Поля для Generic Relations привязываем характеристики
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    attributes = GenericForeignKey('content_type', 'object_id')

    # Добавляем GenericRelation для обратных запросов
    dresses_attributes = GenericRelation(
        'DressesAttributes',
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='tovar'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = ('Товар')
        verbose_name_plural = ('Товары')



    def __str__(self):
        """Return title and username."""
        return str(self.h1)

    def get_absolute_url(self):
        return reverse('tovar_detail', kwargs={'slug_category': self.category.slug, 'slug_tovar': self.slug})

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.title)
        while TovarShop.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = increment_slug_tovar(self.slug, self)
        super(TovarShop, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(TovarShop, self).save(*args, **kwargs)

#Модель Фтогалерреи
def get_file_image_foto(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/tovar', str(instance.tovar.id), filename)

class TovarGallery(models.Model):
    tovar = models.ForeignKey(TovarShop, verbose_name='Тур', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_file_image_foto, verbose_name="Фото")
    alt  = models.CharField(max_length=1000, verbose_name="Тег ALT", blank=True)

    class Meta:
        ordering = ('tovar',)
        verbose_name = ('Фото')
        verbose_name_plural = ('Фото')

    def save(self, *args, **kwargs):
        if not self.tovar_id:
            # Если товар еще не сохранен, сначала сохраняем его
            self.tovar.save()
        super(TovarGallery, self).save(*args, **kwargs)


