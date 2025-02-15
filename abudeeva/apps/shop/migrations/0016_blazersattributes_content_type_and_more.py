# Generated by Django 5.1.4 on 2025-01-14 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('shop', '0015_alter_blazersattributes_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blazersattributes',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='blazersattributes',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dressesattributes',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='dressesattributes',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
