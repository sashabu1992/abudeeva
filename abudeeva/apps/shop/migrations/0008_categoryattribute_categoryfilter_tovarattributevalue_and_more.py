# Generated by Django 5.1.4 on 2025-01-14 16:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_tovargallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название характеристики')),
                ('type', models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('boolean', 'Boolean')], max_length=50, verbose_name='Тип характеристики')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='shop.categoryshop', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Характеристика категории',
                'verbose_name_plural': 'Характеристики категорий',
            },
        ),
        migrations.CreateModel(
            name='CategoryFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название фильтра')),
                ('type', models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('boolean', 'Boolean')], max_length=50, verbose_name='Тип фильтра')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='shop.categoryshop', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Фильтр категории',
                'verbose_name_plural': 'Фильтры категорий',
            },
        ),
        migrations.CreateModel(
            name='TovarAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.categoryattribute', verbose_name='Характеристика')),
                ('tovar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_values', to='shop.tovarshop', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Значение характеристики товара',
                'verbose_name_plural': 'Значения характеристик товаров',
            },
        ),
        migrations.CreateModel(
            name='TovarFilterValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.categoryfilter', verbose_name='Фильтр')),
                ('tovar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_values', to='shop.tovarshop', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Значение фильтра товара',
                'verbose_name_plural': 'Значения фильтров товаров',
            },
        ),
    ]
