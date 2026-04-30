from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Calificacion
from .forms import CalificacionForm, RegistroForm
# ════════════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ════════════════════════════════════════════════════════════════════
def registro_view(request):
    """Registrar un nuevo usuario."""
    if request.user.is_authenticated:
        return redirect('listar')
    form = RegistroForm()
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya existe.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                messages.success(request, f'Bienvenido {username}! Cuenta creada exitosamente.')
                return redirect('listar')
    return render(request, 'registration/register.html', {'form': form})
def login_view(request):
    """Iniciar sesión."""
    if request.user.is_authenticated:
       return redirect('listar')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('listar')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'registration/login.html')
def logout_view(request):
 """Cerrar sesión."""
 logout(request)
 return redirect('login')
# ════════════════════════════════════════════════════════════════════
# CRUD DE CALIFICACIONES
# ════════════════════════════════════════════════════════════════════
@login_required
def listar_view(request):
    """Listar todas las calificaciones."""
    calificaciones = Calificacion.objects.all()
    return render(request, 'calificaciones/listar.html', {
        'calificaciones': calificaciones,
    })
@login_required
def crear_view(request):
    """Crear una nueva calificación."""
    form = CalificacionForm()
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save() # save() del modelo calcula el promedio
            messages.success(request, 'Calificación registrada correctamente.')
            return redirect('listar')
    return render(request, 'calificaciones/crear.html', {'form': form})

@login_required
def editar_view(request, pk):
    """Editar una calificación existente."""
    calificacion = get_object_or_404(Calificacion, pk=pk)
    form = CalificacionForm(instance=calificacion)
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Calificación actualizada correctamente.')
            return redirect('listar')
    return render(request, 'calificaciones/editar.html', {'form': form,
'calificacion': calificacion})

@login_required
def eliminar_view(request, pk):
    """Eliminar una calificación."""
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        calificacion.delete()
        messages.success(request, 'Calificación eliminada correctamente.')
        return redirect('listar')
    return render(request, 'calificaciones/eliminar.html', {'calificacion': calificacion})

@login_required
def promedio_general_view(request):
    """Mostrar el promedio general de todos los estudiantes."""
    promedio_general = Calificacion.objects.all().aggregate(
        Avg('promedio')
    )['promedio__avg']
    calificaciones = Calificacion.objects.all()
    return render(request, 'calificaciones/promedio_general.html', {
        'promedio_general': promedio_general,
 'calificaciones' : calificaciones,
 })