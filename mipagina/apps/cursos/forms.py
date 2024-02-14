from django import forms 
from .models import Alumnos, Asistencia, Cursos





class FormAlumno(forms.ModelForm):
    class Meta:
        model = Alumnos
        exclude = ['curso']
        
        
        
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['alumno', 'presente']
        

class CursoForm(forms.ModelForm):
    class Meta:
        model = Cursos
        fields = ['nombre_del_curso', 'profesor']