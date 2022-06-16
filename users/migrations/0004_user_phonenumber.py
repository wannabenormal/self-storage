# Generated by Django 3.2.13 on 2022-06-16 14:47

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, default='+79788888888', max_length=128, region=None, verbose_name='номер телефона'),
            preserve_default=False,
        ),
    ]
