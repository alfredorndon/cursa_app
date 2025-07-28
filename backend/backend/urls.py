from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importa tus ViewSets de tu app malla_curricular
# Asegúrate de que las clases UsuarioViewSet, UniversidadViewSet, etc.,
# estén correctamente definidas en malla_curricular/views.py
from malla_curricular.views import (
    UsuarioViewSet, UniversidadViewSet, PeriodoViewSet,
    CarreraViewSet, MateriaViewSet, MateriaUsuarioViewSet
)

# Configura el Router de DRF para tus ViewSets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'universidades', UniversidadViewSet)
router.register(r'periodos', PeriodoViewSet)
router.register(r'carreras', CarreraViewSet)
router.register(r'materias', MateriaViewSet)
router.register(r'mi-progreso', MateriaUsuarioViewSet, basename='materiausuario')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta línea incluye todas las URLs generadas por tus ViewSets de DRF bajo /api/
    path('api/', include(router.urls)),
    # Esta línea es para las URLs de autenticación de DRF, como /api-auth/login/ y /api-auth/logout/
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]