# Generated by Django 3.2.13 on 2022-06-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storages', '0007_merge_0006_alter_order_renter_0006_auto_20220618_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='number',
            field=models.CharField(max_length=20, unique=True, verbose_name='номер'),
        ),
    ]
