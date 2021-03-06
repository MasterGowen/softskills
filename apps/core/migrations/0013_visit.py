# Generated by Django 2.1 on 2018-10-19 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_diagnostic_render_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ManyToManyField(to='core.Event')),
                ('person', models.ManyToManyField(to='core.Person')),
                ('project', models.ManyToManyField(to='core.Project')),
            ],
        ),
    ]
