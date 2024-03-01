from django.shortcuts import render

def index(request):
    template_name = 'index.html'
    nombres = ['Juan','Pedro','Federico']
    contexto = {'nombres':nombres}
    return render(request,template_name,contexto)
