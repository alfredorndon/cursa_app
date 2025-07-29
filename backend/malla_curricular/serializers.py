# backend/malla_curricular/serializers.py
from rest_framework import serializers
from .models import Usuario, Universidad, Periodo, Carrera, Materia, MateriaUsuario

# Serializador para el usuario (si quieres exponerlo via API, cuidado con los campos sensibles)
class UsuarioSerializer(serializers.ModelSerializer):
    # Puedes añadir 'carrera_actual_nombre' si quieres ver el nombre de la carrera directamente
    # en lugar del ID en el JSON.
    carrera_actual_nombre = serializers.CharField(source='carrera_actual.nombre', read_only=True)

    class Meta:
        model = Usuario
        # Campos que quieres exponer. Evita campos sensibles como 'password'
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'carrera_actual', 'carrera_actual_nombre']
        read_only_fields = ['username'] # El username no se debería cambiar por la API REST

class UniversidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidad
        fields = '__all__' # Expone todos los campos del modelo

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = '__all__'

class CarreraSerializer(serializers.ModelSerializer):
    # Opcional: Para mostrar las materias directamente anidadas en la carrera
    # materias = MateriaSerializer(many=True, read_only=True)
    universidad_nombre = serializers.CharField(source='universidad.nombre', read_only=True)

    class Meta:
        model = Carrera
        fields = '__all__' # Puedes listar ['id', 'nombre', 'codigo', 'total_unidades_credito', 'universidad', 'universidad_nombre']

class MateriaSerializer(serializers.ModelSerializer):
    # Para mostrar los nombres de los prerrequisitos y la carrera directamente
    prerrequisitos_nombres = serializers.StringRelatedField(many=True, source='prerrequisitos', read_only=True)
    carrera_nombre = serializers.CharField(source='carrera.nombre', read_only=True)

    class Meta:
        model = Materia
        # Asegúrate de incluir 'prerrequisitos' para poder asignar IDs de prerrequisitos al crear/actualizar
        fields = '__all__' # O listar los campos específicos ['id', 'nombre', 'codigo', 'unidades_credito', 'semestre_sugerido', 'creditos_prerrequisito', 'prerrequisitos', 'prerrequisitos_nombres', 'carrera', 'carrera_nombre']

class MateriaUsuarioSerializer(serializers.ModelSerializer):
    # Para mostrar los nombres del usuario y la materia en lugar de solo IDs
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)
    materia_codigo = serializers.CharField(source='materia.codigo', read_only=True)

    class Meta:
        model = MateriaUsuario
        # Incluye los IDs para crear/actualizar, y los nombres para leer
        fields = ['id', 'usuario', 'usuario_username', 'materia', 'materia_nombre', 'materia_codigo', 'estado']
        # unique_together ya está configurado en el modelo, DRF lo respetará automáticamente
        # read_only_fields = ['usuario'] # Si el usuario se asigna automáticamente (ej. desde la solicitud)