# Generated by Django 4.2.6 on 2023-12-24 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_alter_item_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
