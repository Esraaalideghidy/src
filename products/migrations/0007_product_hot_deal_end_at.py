# Generated by Django 5.1.6 on 2025-06-23 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_is_hot_deal'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hot_deal_end_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
