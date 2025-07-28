# backend/malla_curricular/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Universidad, Periodo, Carrera, Materia, MateriaUsuario

# Registra tu modelo de Usuario personalizado
@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    # Campos que quieres que se muestren en la lista de usuarios
    list_display = BaseUserAdmin.list_display + ('carrera_actual',)
    # Campos que quieres poder editar en el formulario de usuario
    fieldsets = BaseUserAdmin.fieldsets + (
        (('Información Adicional', {'fields': ('carrera_actual',)}),)
    )
    # Puedes añadir filtros, búsqueda, etc.
    # list_filter = BaseUserAdmin.list_filter + ('carrera_actual',)
    # search_fields = BaseUserAdmin.search_fields + ('carrera_actual__nombre',)

@admin.register(Universidad)
class UniversidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'año', 'tipo_periodo')
    list_filter = ('año', 'tipo_periodo')
    search_fields = ('nombre',)

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'total_unidades_credito', 'universidad')
    list_filter = ('universidad',)
    search_fields = ('nombre', 'codigo')
    raw_id_fields = ('universidad',) # Útil si hay muchas universidades

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'unidades_credito', 'semestre_sugerido', 'carrera', 'creditos_prerrequisito')
    list_filter = ('carrera', 'semestre_sugerido')
    search_fields = ('nombre', 'codigo')
    # raw_id_fields = ('carrera',) # Si hay muchas carreras
    filter_horizontal = ('prerrequisitos',) # Mejora la interfaz de selección de M2M en el admin

@admin.register(MateriaUsuario)
class MateriaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'materia', 'estado')
    list_filter = ('usuario', 'materia__carrera', 'estado') # Puedes filtrar por la carrera de la materia
    search_fields = ('usuario__username', 'materia__nombre', 'materia__codigo')
    raw_id_fields = ('usuario', 'materia') # Muy útil para buscar usuarios y materias