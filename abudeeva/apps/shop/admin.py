from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from django import forms
from .models import CategoryShop, TovarShop, TovarGallery
from .specifications.dresses import DressesAttributes
from .specifications.general import  Color,Size
from .specifications.blazers import BlazersAttributes
from django.contrib.contenttypes.admin import GenericStackedInline

admin.site.register(Size)
admin.site.register(Color)




@admin.register(CategoryShop)
class CategoryShopAdmin(DjangoMpttAdmin):
    search_fields = ('h1',)
    list_display = ('indented_title', 'created', 'is_draft',)
    fieldsets = (
        ('SEO', {
            'fields': ('title', 'description', 'slug')
        }),
        ('Содержимое', {
            'fields': ('h1',)
        }),
        ('Настройки', {
            'fields': ('parent', 'attribute_type', 'created', 'modified', 'is_draft')
        }),
    )
    readonly_fields = ('created', 'modified')
    list_filter = ('is_draft',)
    prepopulated_fields = {'slug': ('title',)}

    def indented_title(self, obj):
        """
        Добавляет отступы для подкатегорий в зависимости от уровня вложенности.
        """
        return format_html(
            '<div style="padding-left: {}px">{}</div>',
            obj.level * 25,  # 25px отступа на каждый уровень вложенности
            obj.h1
        )
    indented_title.short_description = 'Категория'


class TovarGalleryInline(admin.TabularInline):  # Или используйте StackedInline
    model = TovarGallery
    extra = 1  # Количество пустых форм для добавления новых фотографий
    readonly_fields = ('image_preview',)  # Добавляем поле для предпросмотра

    def image_preview(self, obj):
        """
        Возвращает HTML-код для отображения миниатюры изображения.
        """
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Предпросмотр'

class TovarShopForm(forms.ModelForm):
    class Meta:
        model = TovarShop
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Убедитесь, что поле content_type доступно в форме
        if 'content_type' not in self.fields:
            self.fields['content_type'] = forms.ModelChoiceField(
                queryset=ContentType.objects.all(),
                required=False,
                label='Тип характеристик'
            )

        if 'category' in self.data:
            category_id = self.data['category']
            try:
                category = CategoryShop.objects.get(id=category_id)
                if category.attribute_type == 'dresses':
                    self.fields['content_type'].initial = ContentType.objects.get_for_model(DressesAttributes)
                elif category.attribute_type == 'blazers':
                    self.fields['content_type'].initial = ContentType.objects.get_for_model(BlazersAttributes)
            except (ValueError, CategoryShop.DoesNotExist):
                pass


class DressesAttributesInline(GenericStackedInline):
    model = DressesAttributes
    filter_horizontal = ('colors', 'sizes')  # Указываем поля ManyToManyField
    extra = 0
    max_num = 1

    def has_add_permission(self, request, obj=None):
        # Запретить добавление новых записей, если объект уже существует
        if obj and obj.attributes:
            return False
        return super().has_add_permission(request, obj)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Кастомизация поля sizes
        if db_field.name == "sizes":
            formfield = super().formfield_for_manytomany(db_field, request, **kwargs)
            if formfield.queryset:
                # Добавляем HTML для предпросмотра цвета
                formfield.label_from_instance = lambda obj: format_html(
                    '{} <div style="width: 20px; height: 20px; background-color: {}; display: inline-block; margin-left: 10px;"></div>',
                    obj.code, obj.name
                )
            return formfield

        # Кастомизация поля colors
        if db_field.name == "colors":
            formfield = super().formfield_for_manytomany(db_field, request, **kwargs)
            if formfield.queryset:
                # Добавляем HTML для предпросмотра цвета
                formfield.label_from_instance = lambda obj: format_html(
                    '{} <div style="width: 20px; height: 20px; background-color: {}; display: inline-block; margin-left: 10px;"></div>',
                    obj.name, obj.code
                )
            return formfield

        return super().formfield_for_manytomany(db_field, request, **kwargs)
class BlazersAttributesInline(GenericStackedInline):
    model = BlazersAttributes
    extra = 0
    max_num = 1

    def has_add_permission(self, request, obj=None):
        # Запретить добавление новых записей, если объект уже существует
        if obj and obj.attributes:
            return False
        return super().has_add_permission(request, obj)

@admin.register(TovarShop)
class TovarShopAdmin(admin.ModelAdmin):
    form = TovarShopForm
    search_fields = ('h1',)
    list_display = ('h1', 'price', 'old_price', 'category', 'image_preview', 'created', 'is_draft',)
    fieldsets = (
        ('SEO', {
            'fields': ('title', 'description', 'slug')
        }),
        ('Содержимое', {
            'fields': ('h1', 'zast', 'article', 'price', 'old_price', 'category')
        }),
        ('Настройки', {
            'fields': ('created', 'modified', 'is_draft')
        }),
    )
    readonly_fields = ('created', 'modified')
    list_filter = ('is_draft', 'category',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TovarGalleryInline]

    def get_inlines(self, request, obj=None):
        """
        Возвращает inline-формы в зависимости от типа категории товара.
        """
        if obj and obj.category:
            if obj.category.attribute_type == 'dresses':
                return [DressesAttributesInline, TovarGalleryInline]
            elif obj.category.attribute_type == 'blazers':
                return [BlazersAttributesInline, TovarGalleryInline]
        return [TovarGalleryInline]

    def image_preview(self, obj):
        if obj.zast:  # Проверяем, есть ли изображение в поле zast
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.zast.url
            )
        return "Нет изображения"

    image_preview.short_description = 'Фото'