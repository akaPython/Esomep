from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import DepartamentoListView, DepartamentoCreateView, DepartamentoUpdateView, DepartamentoDeleteView
from .views import EmpleadoListView, BienListView

urlpatterns = [
    path('', views.index, name='index'),

    # URLs para Bien
    path('bienes/', views.BienListView.as_view(), name='bien_list'),
    path('bienes/nuevo/', views.BienCreateView.as_view(), name='bien_create'),
    path('bienes/<int:pk>/editar/', views.BienUpdateView.as_view(), name='bien_update'),
    path('bienes/<int:pk>/eliminar/', views.BienDeleteView.as_view(), name='bien_delete'),
    path('bienes/<int:bien_id>/', views.bien_descripcion, name='bien_descripcion'),
    path('bienes/pdf/', views.pdf_bienes, name='pdf_bienes'),

    # URLs para Cargo
    path('cargos/', views.CargoListView.as_view(), name='cargo_list'),
    path('cargos/nuevo/', views.CargoCreateView.as_view(), name='cargo_create'),
    path('<int:pk>/editar/', DepartamentoUpdateView.as_view(), name='departamento_update'),
    path('<int:pk>/eliminar/', DepartamentoDeleteView.as_view(), name='departamento_delete'),

    # URLs para Departamento
    path('departamentos/', views.DepartamentoListView.as_view(), name='departamento_list'),
    path('departamentos/nuevo/', views.DepartamentoCreateView.as_view(), name='departamento_create'),
    path('departamentos/<int:pk>/editar/', views.DepartamentoUpdateView.as_view(), name='departamento_update'),
    path('departamentos/<int:pk>/eliminar/', views.DepartamentoDeleteView.as_view(), name='departamento_delete'),

    #####################################################################

    #Solicitud
    path('crear-solicitud/', views.crear_solicitud, name='crear_solicitud'),
    path('lista-solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),
    path('procesar-solicitud/<int:id_solicitud>/', views.procesar_solicitud, name='procesar_solicitud'),
    path('solicitudes/', views.lista_solicitudes, name='lista_solicitudes'),


    path('notificaciones/', views.ver_notificaciones, name='ver_notificaciones'),
    path('notificaciones/marcar-leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    
    
    


    ##########################################################################

    path('empleados/', EmpleadoListView.as_view(), name='empleado_list'),

]
