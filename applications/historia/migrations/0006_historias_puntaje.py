# Generated by Django 3.0.5 on 2021-03-09 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historia', '0005_auto_20210309_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='historias',
            name='puntaje',
            field=models.PositiveIntegerField(default=0, verbose_name='puntaje'),
        ),
    ]