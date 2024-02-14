# Generated by Django 4.2.3 on 2023-12-21 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0007_cursos_alumnos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cursos',
            name='alumnos',
        ),
        migrations.AddField(
            model_name='alumnos',
            name='cursos',
            field=models.ManyToManyField(related_name='alumnos', to='cursos.cursos'),
        ),
    ]
