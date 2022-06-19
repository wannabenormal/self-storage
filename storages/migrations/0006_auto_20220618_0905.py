# Generated by Django 3.2.13 on 2022-06-18 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storages', '0005_merge_0004_auto_20220616_1308_0004_auto_20220616_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=100, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='order',
            name='need_delivery',
            field=models.BooleanField(default=False, verbose_name='нужна доставка?'),
        ),
    ]
