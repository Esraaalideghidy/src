# Generated by Django 5.1.6 on 2025-07-12 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
