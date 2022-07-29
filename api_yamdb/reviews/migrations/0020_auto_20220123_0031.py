# Generated by Django 2.2.16 on 2022-01-22 21:31

from django.db import migrations, models

import core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_auto_20220123_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[core.validators.year_validator], verbose_name='Год выпуска'),
        ),
    ]