# Generated by Django 5.0.6 on 2024-07-28 00:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bien',
            fields=[
                ('id_bien', models.AutoField(primary_key=True, serialize=False)),
                ('grupo', models.IntegerField()),
                ('sub_grupo', models.IntegerField()),
                ('seccion', models.IntegerField()),
                ('concepto_de_movimiento', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('stock_minimo', models.IntegerField()),
                ('stock_maximo', models.IntegerField()),
                ('numero_de_identificacion', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=200)),
                ('marca', models.CharField(max_length=200)),
                ('modelo', models.CharField(max_length=200)),
                ('tipo_de_bien', models.CharField(max_length=200)),
                ('numero_inventario', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('material', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=200)),
                ('serie', models.CharField(max_length=200)),
                ('observacion', models.CharField(max_length=200)),
                ('conclusion', models.CharField(max_length=200)),
                ('incorporacion', models.IntegerField()),
                ('desincorporacion', models.IntegerField()),
                ('archivo_multimedia', models.CharField(max_length=255)),
                ('fecha_de_registro', models.DateField()),
                ('estado_actual', models.CharField(choices=[('activo', 'Activo'), ('en_revision', 'En Revisión'), ('resguardado', 'Resguardado'), ('desincorporado', 'Desincorporado')], default='activo', max_length=15)),
                ('esta_archivado', models.BooleanField(default=False)),
                ('fecha_desincorporacion', models.DateField(blank=True, null=True)),
                ('motivo_desincorporacion', models.TextField(blank=True)),
                ('destino_final', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('cargo_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('departamento_id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=50)),
                ('nombre_del_departamento', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RolUsuario',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('id_descripcion', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=150)),
                ('estado', models.CharField(choices=[('bueno', 'Bueno'), ('malo', 'Malo'), ('regular', 'Regular'), ('no existe', 'No existe')], max_length=20)),
                ('id_bien', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aplicacion.bien')),
            ],
        ),
        migrations.AddField(
            model_name='bien',
            name='ubicacion_actual',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bienes', to='aplicacion.departamento'),
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id_empleado', models.AutoField(primary_key=True, serialize=False)),
                ('cedula', models.CharField(max_length=20)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo'), ('otro', 'Otro')], max_length=8)),
                ('telefono', models.CharField(max_length=20)),
                ('fecha_de_ingreso', models.DateField()),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.cargo')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='ProcesoDesincorporacion',
            fields=[
                ('id_proceso', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_solicitud', models.DateField()),
                ('estado_proceso', models.CharField(choices=[('solicitado', 'Solicitado'), ('en_revision', 'En Revisión'), ('aprobado_local', 'Aprobado Local'), ('aprobado_nacional', 'Aprobado Nacional'), ('rechazado', 'Rechazado'), ('completado', 'Completado')], default='solicitado', max_length=20)),
                ('fecha_revision', models.DateField(blank=True, null=True)),
                ('fecha_aprobacion_local', models.DateField(blank=True, null=True)),
                ('fecha_aprobacion_nacional', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True)),
                ('id_bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.bien')),
                ('revisado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='desincorporaciones_revisadas', to='aplicacion.empleado')),
                ('solicitado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='desincorporaciones_solicitadas', to='aplicacion.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Resguardo',
            fields=[
                ('id_resguardo', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('ubicacion', models.CharField(max_length=200)),
                ('motivo', models.TextField()),
                ('id_bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.bien')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id_solicitud', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_de_solicitud', models.CharField(choices=[('traslado_permanente', 'Traslado Permanente'), ('traslado_temporal', 'Traslado Temporal'), ('desincorporacion', 'Desincorporación')], max_length=20)),
                ('descripcion_de_solicitud', models.CharField(max_length=200)),
                ('fecha_de_salida', models.DateField()),
                ('fecha_de_entrega', models.DateField()),
                ('estado_solicitud', models.CharField(choices=[('en_revision', 'En Revisión'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], max_length=11)),
                ('fecha_procesamiento', models.DateField(blank=True, null=True)),
                ('id_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.empleado')),
                ('procesado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitudes_procesadas', to='aplicacion.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudBien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('id_bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.bien')),
                ('id_solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.solicitud')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=255)),
                ('id_empleado', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='aplicacion.empleado')),
                ('id_rol', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='aplicacion.rolusuario')),
            ],
        ),
    ]
