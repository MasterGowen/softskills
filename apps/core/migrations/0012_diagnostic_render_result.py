# Generated by Django 2.1 on 2018-10-16 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_diagnostic_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostic',
            name='render_result',
            field=models.TextField(blank=True, null=True, verbose_name='Функция отрисовки ответа'),
        ),
    ]