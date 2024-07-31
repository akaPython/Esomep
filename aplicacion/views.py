from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import (
    Bien, Cargo, Departamento, Caracteristica, Empleado, RolUsuario,
    Solicitud, SolicitudBien, Usuario, Resguardo, Notificacion
)
from .forms import (
    BienForm, CargoForm, DepartamentoForm, CaracteristicaForm, EmpleadoForm,
    RolUsuarioForm, SolicitudForm, UsuarioForm, SolicitudBienForm, EmpleadoRegistroForm, ResguardoForm
)
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin



###############################################################################################################

@login_required
def index(request):
    context = {}
    if request.user.is_authenticated and hasattr(request.user, 'empleado'):
        context['has_unread_notifications'] = request.user.empleado.notificaciones.filter(leida=False).exists()
    return render(request, 'index.html', context)






class BienListView(LoginRequiredMixin, ListView):
    model = Bien
    template_name = 'bien_list.html'
    context_object_name = 'bienes'


class BienCreateView(LoginRequiredMixin, CreateView):
    model = Bien
    form_class = BienForm
    template_name = 'bien_form.html'
    success_url = reverse_lazy('bien_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departamentos'] = Departamento.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        bien = form.save(commit=False)

        departamento_id = self.request.POST.get('ubicacion_actual')
        if departamento_id:
            bien.ubicacion_actual = Departamento.objects.get(pk=departamento_id)

        bien.save()

        descripciones = self.request.POST.getlist('descripcion[]')
        estados = self.request.POST.getlist('estado[]')

        for descripcion, estado in zip(descripciones, estados):
            Caracteristica.objects.create(
                id_bien=bien,
                descripcion=descripcion,
                estado=estado
            )

        return redirect(self.success_url)

    def form_invalid(self, form):
        print(form.errors)  # Registra los errores del formulario
        return self.render_to_response(self.get_context_data(form=form))



class BienUpdateView(LoginRequiredMixin, UpdateView):
    model = Bien
    form_class = BienForm
    template_name = 'bien_form.html'
    success_url = reverse_lazy('bien_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departamentos'] = Departamento.objects.all()
        context['caracteristicas'] = Caracteristica.objects.filter(id_bien=self.object)
        return context

    def form_valid(self, form):
        bien = form.save(commit=False)

        departamento_id = self.request.POST.get('ubicacion_actual')
        if departamento_id:
            bien.ubicacion_actual = Departamento.objects.get(pk=departamento_id)

        bien.save()

        # Eliminar características existentes y crear nuevas
        Caracteristica.objects.filter(id_bien=bien).delete()

        descripciones = self.request.POST.getlist('descripcion[]')
        estados = self.request.POST.getlist('estado[]')

        for descripcion, estado in zip(descripciones, estados):
            if descripcion.strip():  # Solo crea si la descripción no está vacía
                Caracteristica.objects.create(
                    id_bien=bien,
                    descripcion=descripcion,
                    estado=estado
                )

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        # Añade los valores iniciales para los campos que no son parte del modelo Bien
        if self.object:
            initial['ubicacion_actual'] = self.object.ubicacion_actual.pk if self.object.ubicacion_actual else None
        return initial


class BienDeleteView(LoginRequiredMixin, DeleteView):
    model = Bien
    template_name = 'bien_confirm_delete.html'
    success_url = reverse_lazy('bien_list')


class CargoListView(LoginRequiredMixin, ListView):
    model = Cargo
    template_name = 'cargo_list.html'
    context_object_name = 'cargos'


class CargoCreateView(LoginRequiredMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargo_form.html'
    success_url = reverse_lazy('cargo_list')


class CargoUpdateView(LoginRequiredMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargo_form.html'
    success_url = reverse_lazy('cargo_list')


class CargoDeleteView(LoginRequiredMixin, DeleteView):
    model = Cargo
    template_name = 'cargo_confirm_delete.html'
    success_url = reverse_lazy('cargo_list')


class DepartamentoListView(LoginRequiredMixin, ListView):
    model = Departamento
    template_name = 'departamento_list.html'
    context_object_name = 'departamentos'


class DepartamentoCreateView(LoginRequiredMixin, CreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'departamento_form.html'
    success_url = reverse_lazy('departamento_list')


class DepartamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'departamento_form.html'
    success_url = reverse_lazy('departamento_list')


class DepartamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Departamento
    template_name = 'departamento_confirm_delete.html'
    success_url = reverse_lazy('departamento_list')

@login_required
def solicitud_detail(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    if request.method == 'POST':
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('solicitud_list')
    else:
        form = SolicitudForm(instance=solicitud)
    return render(request, 'solicitud_detail.html', {'form': form, 'solicitud': solicitud})

@login_required
def bien_descripcion(request, bien_id):
    bien = get_object_or_404(Bien, id_bien=bien_id)
    caracteristicas = Caracteristica.objects.filter(id_bien=bien)
    return render(request, 'descripcion_bien.html', {'bien': bien, 'caracteristicas': caracteristicas})


##############################################################################################################

@login_required
def pdf_bienes(request):
    bienes = Bien.objects.all()
    html_string = render_to_string('pdf.html', {'bienes': bienes})
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="lista_bienes.pdf"'
    return response

##############################################################################################################


@login_required
def crear_solicitud(request):
    if request.method == 'POST':
        form_solicitud = SolicitudForm(request.POST)
        if form_solicitud.is_valid():
            solicitud = form_solicitud.save(commit=False)
            solicitud.empleado = request.user.empleado
            solicitud.save()
            
            # Notificar al jefe de bienes
            jefes_bienes = Empleado.objects.filter(es_jefe_bienes=True)
            for jefe in jefes_bienes:
                Notificacion.objects.create(
                    empleado=jefe,
                    mensaje=f"Nueva solicitud creada por {solicitud.empleado.nombres} {solicitud.empleado.apellidos}. Tipo: {solicitud.tipo_de_solicitud}. ID: {solicitud.id_solicitud}"
                )
            
            return redirect('lista_solicitudes')
    else:
        form_solicitud = SolicitudForm()
    
    return render(request, 'crear_solicitud.html', {'form_solicitud': form_solicitud})


@login_required
def lista_solicitudes(request):
    if request.user.empleado.es_jefe_bienes:
        solicitudes = Solicitud.objects.filter(estado_solicitud='en_revision')
    else:
        solicitudes = Solicitud.objects.filter(empleado=request.user.empleado)
    return render(request, 'lista_solicitudes.html', {'solicitudes': solicitudes})

@login_required
def procesar_solicitud(request, id_solicitud):
    solicitud = get_object_or_404(Solicitud, id_solicitud=id_solicitud)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        bien_id = request.POST.get('bien_id')

        if bien_id:
            try:
                bien = Bien.objects.get(id_bien=bien_id)
            except Bien.DoesNotExist:
                return render(request, 'procesar_solicitud.html', {'solicitud': solicitud, 'error': 'El bien no existe.'})
        else:
            bien = None

        if accion == 'aceptar':
            solicitud.estado_solicitud = 'aceptada'
            if solicitud.tipo_de_solicitud in ['traslado_permanente', 'traslado_temporal'] and bien:
                bien.ubicacion_actual = solicitud.empleado.departamento
                bien.save()
            elif solicitud.tipo_de_solicitud == 'desincorporacion' and bien:
                bien.estado_actual = 'en_revision'
                bien.save()
                # Iniciar proceso de desincorporación
            
            # Notificar al empleado que su solicitud fue aceptada
            Notificacion.objects.create(
                empleado=solicitud.empleado,
                mensaje=f"Su solicitud de {solicitud.tipo_de_solicitud} ha sido aceptada."
            )
        else:
            solicitud.estado_solicitud = 'rechazada'
            solicitud.motivo_rechazo = request.POST.get('motivo_rechazo', '')
            
            # Notificar al empleado que su solicitud fue rechazada
            Notificacion.objects.create(
                empleado=solicitud.empleado,
                mensaje=f"Su solicitud de {solicitud.tipo_de_solicitud} ha sido rechazada. Motivo: {solicitud.motivo_rechazo}"
            )
        
        solicitud.procesado_por = request.user.empleado
        solicitud.fecha_procesamiento = timezone.now()
        solicitud.save()
        
        return redirect('lista_solicitudes')
    
    return render(request, 'procesar_solicitud.html', {'solicitud': solicitud})


@login_required
def ver_notificaciones(request):
    notificaciones = Notificacion.objects.filter(empleado=request.user.empleado, leida=False)
    
    for notificacion in notificaciones:
        if 'Nueva solicitud creada' in notificacion.mensaje:
            try:
                id_solicitud = int(notificacion.mensaje.split('ID:')[-1].strip())
                notificacion.id_solicitud = id_solicitud
            except ValueError:
                notificacion.id_solicitud = None
        else:
            notificacion.id_solicitud = None
    
    return render(request, 'notificaciones.html', {
        'notificaciones': notificaciones,
        'user': request.user
    })

@login_required
def marcar_notificacion_leida(request, notificacion_id):
    notificacion = Notificacion.objects.get(id=notificacion_id)
    if notificacion.empleado == request.user.empleado:
        notificacion.leida = True
        notificacion.save()
    return redirect('ver_notificaciones')




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



def registro(request):
    if request.method == 'POST':
        form = EmpleadoRegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = EmpleadoRegistroForm()
    return render(request, 'registro.html', {'form': form})
@login_required
def lista_solicitudes(request):
    if request.user.empleado.es_jefe_bienes:
        solicitudes = Solicitud.objects.all()
    else:
        solicitudes = Solicitud.objects.filter(empleado=request.user.empleado)
    return render(request, 'lista_solicitudes.html', {'solicitudes': solicitudes})



class EmpleadoListView(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'empleado_list.html'
    context_object_name = 'empleados'
    paginate_by = 10  # Puedes ajustar esto según sea necesario