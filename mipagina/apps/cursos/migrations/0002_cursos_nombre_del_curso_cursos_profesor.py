# Generated by Django 4.2.7 on 2023-11-11 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cursos',
            name='nombre_del_curso',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cursos',
            name='profesor',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
