# Generated by Django 5.0.6 on 2024-05-11 04:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_product_category_product_foo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='foo',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.category'),
        ),
    ]
