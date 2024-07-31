from django.db import models
from django.contrib.auth.models import User

class Departamento(models.Model):
    departamento_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50)
    nombre_del_departamento = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

class Bien(models.Model):
    ESTADO_BIEN_CHOICES = [
        ('activo', 'Activo'),
        ('en_revision', 'En Revisión'),
        ('resguardado', 'Resguardado'),
        ('desincorporado', 'Desincorporado'),
    ]

    id_bien = models.AutoField(primary_key=True)
    grupo = models.IntegerField()
    sub_grupo = models.IntegerField()
    seccion = models.IntegerField()
    concepto_de_movimiento = models.IntegerField()
    cantidad = models.IntegerField()
    stock = models.IntegerField()
    stock_minimo = models.IntegerField()
    stock_maximo = models.IntegerField()
    numero_de_identificacion = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    tipo_de_bien = models.CharField(max_length=200)
    numero_inventario = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)
    serie = models.CharField(max_length=200)
    observacion = models.CharField(max_length=200)
    conclusion = models.CharField(max_length=200)
    incorporacion = models.IntegerField()
    desincorporacion = models.IntegerField()
    archivo_multimedia = models.CharField(max_length=255)
    fecha_de_registro = models.DateField()
    ubicacion_actual = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, related_name='bienes')
    estado_actual = models.CharField(max_length=15, choices=ESTADO_BIEN_CHOICES, default='activo')
    fecha_desincorporacion = models.DateField(null=True, blank=True)
    motivo_desincorporacion = models.TextField(blank=True)

class Cargo(models.Model):
    cargo_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

class Caracteristica(models.Model):
    ESTADO_CHOICES = [
        ('bueno', 'Bueno'),
        ('malo', 'Malo'),
        ('regular', 'Regular'),
        ('no existe', 'No existe'),
    ]

    id_descripcion = models.AutoField(primary_key=True)
    id_bien = models.ForeignKey(Bien, on_delete=models.CASCADE, null=True)
    descripcion = models.CharField(max_length=150)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)

class Empleado(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('otro', 'Otro'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    es_jefe_bienes = models.BooleanField(default=False)
    id_empleado = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    estado = models.CharField(max_length=8, choices=ESTADO_CHOICES)
    telefono = models.CharField(max_length=20)
    fecha_de_ingreso = models.DateField()

class RolUsuario(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

class Solicitud(models.Model):
    TIPO_SOLICITUD_CHOICES = [
        ('traslado_permanente', 'Traslado Permanente'),
        ('traslado_temporal', 'Traslado Temporal'),
        ('desincorporacion', 'Desincorporación'),
    ]
    ESTADO_SOLICITUD_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('en_resguardo', 'En Resguardo'),
        ('desincorporado', 'Desincorporado'),
    ]

    id_solicitud = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='solicitudes', null=True)
    tipo_de_solicitud = models.CharField(max_length=20, choices=TIPO_SOLICITUD_CHOICES)
    descripcion_solicitud = models.TextField(null=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, null=True)
    estado_solicitud = models.CharField(max_length=20, choices=ESTADO_SOLICITUD_CHOICES, default='pendiente')
    procesado_por = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes_procesadas')
    fecha_procesamiento = models.DateTimeField(null=True, blank=True)
    motivo_rechazo = models.TextField(blank=True)
    fecha_revision = models.DateField(null=True, blank=True)
    fecha_aprobacion_local = models.DateField(null=True, blank=True)
    fecha_aprobacion_nacional = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    departamento_destino = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes_destino')

class SolicitudBien(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='bienes_solicitados', null=True)
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, null=True, blank=True)
    descripcion_bien = models.TextField(null=True)
    cantidad = models.IntegerField(default=1)

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    id_rol = models.ForeignKey(RolUsuario, on_delete=models.CASCADE, default=1)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, default=1)

class Resguardo(models.Model):
    id_resguardo = models.AutoField(primary_key=True)
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    ubicacion = models.CharField(max_length=200)
    responsable = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    motivo = models.TextField()
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='resguardos', null=True, blank=True)

class Notificacion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)