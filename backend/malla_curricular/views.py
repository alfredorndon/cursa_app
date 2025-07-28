from rest_framework import viewsets, permissions
from .models import Usuario, Universidad, Periodo, Carrera, Materia, MateriaUsuario
from .serializers import (
    UsuarioSerializer, UniversidadSerializer, PeriodoSerializer,
    CarreraSerializer, MateriaSerializer, MateriaUsuarioSerializer
)

# Permisos básicos para ViewSets (puedes ajustarlos según tus necesidades)
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir acceso de lectura a todos,
    pero solo escritura a administradores.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff # Solo si es un usuario staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir a los propietarios de un objeto editarlo.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Asume que el objeto tiene un campo 'usuario' o 'owner'
        return obj.usuario == request.user

# ViewSets para tus modelos
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser] # Solo administradores pueden gestionar usuarios

class UniversidadViewSet(viewsets.ModelViewSet):
    queryset = Universidad.objects.all()
    serializer_class = UniversidadSerializer
    permission_classes = [IsAdminOrReadOnly] # Permite ver a todos, editar solo a admins

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    permission_classes = [IsAdminOrReadOnly]

class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer
    permission_classes = [IsAdminOrReadOnly]

class MateriaViewSet(viewsets.ModelViewSet): # Aquí había un pequeño error de tipeo, corregido a viewsets
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [IsAdminOrReadOnly]

class MateriaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = MateriaUsuario.objects.all()
    serializer_class = MateriaUsuarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly] # Solo autenticados y solo editan sus propios registros

    def get_queryset(self):
        # Filtra para que cada usuario solo vea sus propias MateriaUsuario
        if self.request.user.is_authenticated:
            return MateriaUsuario.objects.filter(usuario=self.request.user)
        return MateriaUsuario.objects.none() # No muestra nada si no está autenticado

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario autenticado al crear MateriaUsuario
        serializer.save(usuario=self.request.user)