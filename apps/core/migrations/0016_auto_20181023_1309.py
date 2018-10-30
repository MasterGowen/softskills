# Generated by Django 2.1 on 2018-10-23 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20181023_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.CharField(choices=[('simple', 'Обычный'), ('minor', 'Майнор')], default='simple', max_length=32, verbose_name='Тип курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='_enddate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Конец курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='_startdate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Начало курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Название курса'),
        ),
    ]
