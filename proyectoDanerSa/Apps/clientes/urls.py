from django.urls import path

from . import views

app_name = "Apps.clientes"
urlpatterns = [
    path('', views.ListaClientesView, name='lista_clientes'),
    path('agregar', views.VistaAgregarCliente, name='agregar_cliente'),
    path('actualizar/<str:id_cliente>/',
        views.VistaActulizarCliente, name='actualizar_cliente'),
    path('eliminar/<str:id_cliente>/',
        views.VistaEliminarCliente, name='eliminar_cliente'),
    path('detalles/<str:id_cliente>/',
        views.DetalleClientesView, name='detalles_clientes'),
    path("get", views.GetClientsAJAXView, name="get_clientes"),




    path('report', views.VistaCliente, name='VistaCliente'),
]

