# Generated by Django 5.1.4 on 2025-01-14 17:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('shop', '0014_remove_tovarshop_content_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blazersattributes',
            options={'verbose_name': 'Характеристики жакета', 'verbose_name_plural': 'Характеристики жакетов'},
        ),
        migrations.AlterModelOptions(
            name='dressesattributes',
            options={'verbose_name': 'Характеристики платья', 'verbose_name_plural': 'Характеристики платьев'},
        ),
        migrations.RemoveField(
            model_name='tovarshop',
            name='blazers_attributes',
        ),
        migrations.RemoveField(
            model_name='tovarshop',
            name='dresses_attributes',
        ),
        migrations.AddField(
            model_name='tovarshop',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='tovarshop',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
