# Generated by Django 5.0 on 2023-12-31 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frugal', '0003_rename_date_updated_favorite_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_store_id',
            field=models.BigIntegerField(default=0),
        ),
    ]
