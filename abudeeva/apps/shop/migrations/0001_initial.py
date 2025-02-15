# Generated by Django 5.1.4 on 2025-01-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URl')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок Title')),
                ('description', models.CharField(blank=True, max_length=350, verbose_name='Описание Description')),
                ('h1', models.CharField(max_length=255, verbose_name='Заголовок H1')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('is_draft', models.BooleanField(default=True, verbose_name='Опубликован')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('title',),
            },
        ),
    ]
