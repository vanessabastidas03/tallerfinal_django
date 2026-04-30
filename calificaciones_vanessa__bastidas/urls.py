from django.urls import path
from . import views

urlpatterns = [
    # ── Autenticación ──────────────────────────────────────────────
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── CRUD de calificaciones ─────────────────────────────────────
    path('calificaciones/', views.listar_view, name='listar'),
    path('calificaciones/crear/', views.crear_view, name='crear'),
    path('calificaciones/editar/<int:pk>/', views.editar_view, name='editar'),
    path('calificaciones/eliminar/<int:pk>/', views.eliminar_view, name='eliminar'),
    
    # ── Vista del promedio general ─────────────────────────────────
    path('promedio-general/', views.promedio_general_view, name='promedio_general'),
]