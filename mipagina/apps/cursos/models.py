from django.db import models
from django.utils import timezone



class Alumnos(models.Model):
    apellido = models.CharField(max_length=50,null=True)
    nombre = models.CharField(max_length=50,null=True)
    numero_de_contacto = models.CharField(max_length=50,null=True)
    adeuda_cuota = models.BooleanField('Adeuda_cuota', default=False)


class Cursos(models.Model):
    nombre_del_curso = models.CharField(max_length=50, null=True)
    profesor = models.CharField(max_length=50, null=True)
    alumnos = models.ManyToManyField('Alumnos', related_name='cursos')


class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    presente = models.BooleanField()

   # class Meta:
    #    unique_together = ('alumno', 'curso', 'fecha')
        

