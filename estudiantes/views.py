from django.shortcuts import render, redirect
from .models import Estudiante
from .forms import EstudianteForm

def inicio(request):
    # POST: recibe formulario; GET: muestra formulario y registros.
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()  # Django guarda en la BD configurada en settings.py
            return redirect('inicio')
    else:
        form = EstudianteForm()
    estudiantes = Estudiante.objects.order_by('-creado_en')
    return render(request, 'estudiantes/inicio.html', {
        'form': form, 'estudiantes': estudiantes,
    })
