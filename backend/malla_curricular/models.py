# backend/malla_curricular/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    carrera_actual = models.ForeignKey(
        'Carrera', # Referencia al modelo Carrera
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='estudiantes',
        verbose_name='Carrera Actual del Estudiante'
    )
    
    class Meta(AbstractUser.Meta):
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'
        swappable='AUTH_USER_MODEL'

    def __str__(self):
        return self.username

class Universidad(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name='Nombre de la Universidad')
    
    class Meta:
        verbose_name='Universidad'
        verbose_name_plural='Universidades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Periodo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre del Período')
    año = models.IntegerField(verbose_name='Año')
    tipo_periodo = models.CharField(
        max_length=50,
        choices=[
            ('regular', 'Regular'),
            ('intensivo', 'Intensivo')
        ],
        default='regular', 
        verbose_name='Tipo de Período'
    )

    class Meta:
        verbose_name='Período' 
        verbose_name_plural='Períodos' 
        unique_together = ('nombre', 'año', 'tipo_periodo') 
        ordering = ['-año', 'nombre'] 

    def __str__(self):
        return f'{self.nombre} ({self.año})' 

class Carrera(models.Model):
    nombre = models.CharField(max_length=250, unique=True, verbose_name='Nombre de la Carrera')
    codigo = models.CharField(max_length=10, unique=True, verbose_name='Código de la Carrera') 
    total_unidades_credito = models.IntegerField(verbose_name='Total Unidades de Crédito') 
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name='carreras', verbose_name='Universidad a la que pertenece') 

    class Meta:
        verbose_name='Carrera'
        verbose_name_plural='Carreras'
        unique_together = ('nombre', 'universidad')
        ordering = ['nombre']
    
    def __str__(self):
        return f'{self.nombre} ({self.universidad.nombre})'

class Materia(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre de la Materia')
    codigo = models.CharField(max_length=15, unique=True, verbose_name='Código de la Materia') 
    unidades_credito = models.IntegerField(verbose_name='Unidades de Crédito') 
    semestre_sugerido = models.IntegerField(blank=True, null=True, verbose_name='Semestre Sugerido') 
    creditos_prerrequisito = models.IntegerField(
        default=0,
        verbose_name='Créditos Prerrequisito Acumulados', 
        help_text='Unidades de crédito mínimas acumuladas para cursar esta materia.' 
    )
    prerrequisitos = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='materia_siguiente',
        verbose_name='Prerrequisitos por Materia',
        help_text='Materias que deben ser cursadas antes.'
    )
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.CASCADE,
        related_name='materias',
        verbose_name='Carrera a la que pertenece'
    )

    class Meta:
        verbose_name='Materia'
        verbose_name_plural='Materias'
        unique_together = ('nombre', 'carrera')
        ordering = ['semestre_sugerido', 'nombre']

    def __str__(self):
        return f'{self.nombre} ({self.codigo})'

class MateriaUsuario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='materias_cursadas'
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name='usuarios_cursando'
    )
    estado = models.CharField(
        max_length=50,
        choices=[
            ('aprobada', 'Aprobada'),
            ('cursando', 'Cursando'),
            ('pendiente', 'Pendiente')
        ],
        default='pendiente',
        verbose_name='Estado de la Materia'
    )

    class Meta:
        verbose_name = 'Materia por Usuario'
        verbose_name_plural = 'Materias por Usuario'
        unique_together = ('usuario', 'materia')
        ordering = ['usuario', 'materia']

    def __str__(self):
        estado_str = self.get_estado_display()
        return f'{self.usuario.username} - {self.materia.nombre} ({estado_str})'