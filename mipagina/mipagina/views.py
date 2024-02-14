from django.shortcuts import render
from apps.cursos.views import ListaDeCursos

def index(request):
    # Utiliza la vista ListaDeCursos para obtener la lista de cursos
    lista_cursos_view = ListaDeCursos()
    cursos = lista_cursos_view.get_queryset()

    # Pasa la lista de cursos como parte del contexto
    context = {'cursos': cursos}

    templates_name = 'index.html'
    return render(request, templates_name, context)

