# Generated by Django 3.2.13 on 2022-06-16 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storage',
            options={'verbose_name': 'Склад', 'verbose_name_plural': 'Склады'},
        ),
        migrations.AddField(
            model_name='box',
            name='floor',
            field=models.SmallIntegerField(default=1, verbose_name='этаж'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storage',
            name='contacts',
            field=models.CharField(blank=True, max_length=50, verbose_name='Контакты'),
        ),
        migrations.AddField(
            model_name='storage',
            name='description',
            field=models.TextField(default=0, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storage',
            name='feature',
            field=models.CharField(blank=True, max_length=50, verbose_name='особенность'),
        ),
    ]
