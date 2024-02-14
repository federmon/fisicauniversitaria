# urls.py de cursos

from django.urls import path
from .views import CursoDetailView, ListaDeCursos, agregar_alumno, eliminar_alumno, BuscarView
from .views import actualizar_asistencia, tomar_asistencia, detalles_curso, asistencia_por_fecha, finalizar_asistencia
from .views import PlanillaAsistenciaListView, detalle_alumno, crear_curso




urlpatterns = [
    
    path('cursos_list/', ListaDeCursos.as_view(), name='cursos'),
    path('curso_detail/<int:pk>/', CursoDetailView.as_view(), name='curso'),
    path('agregar_alumno/<int:curso_id>/', agregar_alumno, name='agregar_alumno'),
    path('curso/<int:curso_id>/eliminar_alumno/<int:alumno_id>/', eliminar_alumno, name='eliminar_alumno'),
    path('buscar/', BuscarView.as_view(), name='buscar'),
    path('curso/<int:curso_id>/asistencia/actualizar/', actualizar_asistencia, name='actualizar_asistencia'),
    path('cursos/curso/<int:curso_id>/asistencia/<int:alumno_id>/', tomar_asistencia, name='tomar_asistencia'),
    path('curso/<int:curso_id>/planilla_asistencia/', PlanillaAsistenciaListView.as_view(), name='planilla_asistencia'),
    path('curso/<int:curso_id>/', detalles_curso, name='detalle_curso'),
    path('asistencia/<int:year>/<int:month>/<int:day>/<int:curso_id>/', asistencia_por_fecha, name='asistencia_por_fecha'),
    path('alumno/<int:id>/curso/<int:curso_id>/', detalle_alumno, name='detalle_alumno'),
    path('crear_curso/', crear_curso, name='crear_curso'),
    path('curso/<int:curso_id>/resultados_asistencia/', finalizar_asistencia, name='resultados_asistencia'),






]
