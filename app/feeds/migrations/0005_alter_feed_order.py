# Generated by Django 3.2 on 2021-05-17 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0004_auto_20210424_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='order',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
