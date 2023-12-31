# Generated by Django 5.0 on 2023-12-31 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frugal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='created_date',
            new_name='date_updated',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='created_date',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='updated_date',
            new_name='date_updated',
        ),
        migrations.AddField(
            model_name='favorite',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]