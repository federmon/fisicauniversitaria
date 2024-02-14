from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views import generic
from .models import Cursos, Alumnos, Asistencia
from .forms import FormAlumno, AsistenciaForm, CursoForm
from django.urls import reverse
from django.forms import modelformset_factory
from django.views.generic import ListView
from .models import Asistencia
from django.utils import timezone
from collections import defaultdict
from django.utils.timezone import datetime
from datetime import date
from django.http import HttpResponseRedirect



    
    
    
class ListaDeCursos(generic.ListView):
    model = Cursos
    template_name = 'cursos_list.html'
    context_object_name = 'cursos'
    
    def get_queryset(self):
        cursos = Cursos.objects.all()
        return cursos


class CursoDetailView(generic.DetailView):
    model = Cursos
    template_name = 'cursos/curso_detail.html'
    context_object_name = 'curso'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = Cursos.objects.all()
        context['todos_los_alumnos'] = Alumnos.objects.all()
        context['alumnos'] = self.object.alumnos.all()
        return context
    
def agregar_alumno(request, curso_id):
    curso = Cursos.objects.get(pk=curso_id)
    
    if request.method == 'POST':
        form = FormAlumno(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.save()
            curso.alumnos.add(alumno)

            return redirect(reverse('curso', kwargs={'pk': curso_id}))
    else:
        form = FormAlumno()
        
    alumnos_del_curso = curso.alumnos.all()

    return render(request, 'cursos/curso_detail.html', {'form': form, 'curso': curso, 'alumnos': alumnos_del_curso})


def eliminar_alumno(request, curso_id, alumno_id):
    curso = get_object_or_404(Cursos, pk=curso_id)
    alumno = get_object_or_404(Alumnos, pk=alumno_id)
    
    # Eliminar al alumno del curso
    curso.alumnos.remove(alumno)
    
    Asistencia.objects.filter(alumno=alumno).delete()
    
    alumno.delete()

    
    return redirect(reverse('curso', kwargs={'pk': curso_id}))
    
   
class BuscarView(View):
    def get(self, request, *args, **kwargs):
        # Obtener el término de búsqueda de la URL
        query = request.GET.get('q', '')

        # Realizar la búsqueda en los modelos Cursos y Alumnos
        resultados_cursos = Cursos.objects.filter(
            nombre_del_curso__icontains=query
        ) | Cursos.objects.filter(
            profesor__icontains=query
        )

        resultados_alumnos = Alumnos.objects.filter(
            apellido__icontains=query
        ) | Alumnos.objects.filter(
            nombre__icontains=query
        )

        # Puedes pasar los resultados a la plantilla
        return render(
            request,
            'resultados_busqueda.html',
            {'query': query, 'resultados_cursos': resultados_cursos, 'resultados_alumnos': resultados_alumnos}
        )    
  


def actualizar_asistencia(request, curso_id):
    curso = get_object_or_404(Cursos, pk=curso_id)

    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planilla_asistencia', curso_id=curso_id)
    else:
        form = AsistenciaForm(initial={'curso': curso})

    return render(request, 'asistencia/formulario.html', {'form': form, 'curso': curso})




# En tu views.py
from django.shortcuts import render, redirect
from .models import Alumnos, Cursos, Asistencia
from django.utils import timezone

def tomar_asistencia(request, curso_id, alumno_id=None):
    curso = get_object_or_404(Cursos, id=curso_id)
    alumnos = curso.alumnos.all()
    fecha_actual = timezone.now().date()

    if not alumno_id:
        alumno_id = alumnos.first().id if alumnos else None

    alumno_actual = get_object_or_404(Alumnos, id=alumno_id) if alumno_id else None

    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            # Buscar si ya existe una entrada de asistencia para este alumno y fecha
            asistencia_obj, created = Asistencia.objects.get_or_create(
                alumno=alumno_actual, curso=curso, fecha=fecha_actual,
                defaults={'presente': form.cleaned_data['presente']}
            )

            # Si la asistencia ya existía, actualizarla
            if not created:
                asistencia_obj.presente = form.cleaned_data['presente']
                asistencia_obj.save()

            # Proceso para pasar al siguiente alumno
            next_alumno_id = alumnos.filter(id__gt=alumno_id).values_list('id', flat=True).first()
            if next_alumno_id:
                return HttpResponseRedirect(reverse('tomar_asistencia', args=[curso_id, next_alumno_id]))
            else:
                # Redirigir al finalizar la toma de asistencia para todos los alumnos
                return HttpResponseRedirect(reverse('resultados_asistencia', args=[curso_id]))

    else:
        form = AsistenciaForm(initial={'alumno': alumno_actual, 'curso': curso}) if alumno_actual else None

    context = {
        'curso': curso,
        'alumno_actual': alumno_actual,
        'form': form,
        'next_alumno_id': alumnos.filter(id__gt=alumno_id).values_list('id', flat=True).first()
    }
    return render(request, 'cursos/tomar_asistencia.html', context)

class PlanillaAsistenciaListView(ListView):
    model = Asistencia
    template_name = 'cursos/planilla_asistencia.html'

    def get_queryset(self):
        curso_id = self.kwargs.get('curso_id')
        return Asistencia.objects.filter(curso__id=curso_id).order_by('fecha')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso_id'] = self.kwargs['curso_id']
        asistencias = self.get_queryset()
        

        asistencias_por_fecha = defaultdict(list)
        for asistencia in asistencias:
            asistencias_por_fecha[asistencia.fecha].append(asistencia)
            
        context['asistencias_por_fecha'] = dict(asistencias_por_fecha)
        return context
    
def asistencia_por_fecha(request, year, month, day, curso_id):
    fecha = datetime(year=year, month=month, day=day)
    asistencias = Asistencia.objects.filter(fecha=fecha, curso_id=curso_id)

    return render(request, 'cursos/asistencia_por_fecha.html', {'asistencias': asistencias, 'fecha': fecha, 'curso_id': curso_id})    
        
def detalles_curso(request, curso_id):
    curso = Cursos.objects.get(id=curso_id)
    alumnos = curso.alumnos.all()
    fecha_actual = timezone.now().date()

    # Contando el total de alumnos
    total_alumnos = alumnos.count()

    # Contando los presentes y ausentes para la fecha actual
    asistencias_hoy = Asistencia.objects.filter(curso=curso, fecha=fecha_actual)
    presentes_hoy = asistencias_hoy.filter(presente=True).count()
    ausentes_hoy = total_alumnos - presentes_hoy

    context = {
        'curso': curso,
        'alumnos': alumnos,  # Agregar esta línea para incluir la lista de alumnos
        'total_alumnos': total_alumnos,
        'presentes_hoy': presentes_hoy,
        'ausentes_hoy': ausentes_hoy,
    }

    return render(request, 'cursos/curso_detail.html', context)


def detalle_alumno(request, id, curso_id):
    alumno = Alumnos.objects.get(id=id)
    curso = Cursos.objects.get(id=curso_id)

    context = {
        'alumno': alumno,
        'curso': curso,  # Añade el curso al contexto
    }

    return render(request, 'cursos/detalle_alumno.html', context)



def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cursos')  # Asegúrate de usar la URL correcta
    else:
        form = CursoForm()

    return render(request, 'cursos/crear_curso.html', {'form': form})

def finalizar_asistencia(request, curso_id):
    curso = Cursos.objects.get(id=curso_id)
    fecha_actual = date.today()
    asistencias = Asistencia.objects.filter(curso=curso, fecha=fecha_actual)  # Asegúrate de filtrar por la fecha actual

    presentes = asistencias.filter(presente=True).count()
    ausentes = asistencias.filter(presente=False).count()
    total = curso.alumnos.count()

    context = {
        'curso': curso,
        'presentes': presentes,
        'ausentes': ausentes,
        'total': total,
    }
    return render(request, 'cursos/resultados_asistencia.html', context)