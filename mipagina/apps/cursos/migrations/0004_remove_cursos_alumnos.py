# Generated by Django 4.2.3 on 2023-12-20 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_alumnos_cursos_alumnos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cursos',
            name='alumnos',
        ),
    ]