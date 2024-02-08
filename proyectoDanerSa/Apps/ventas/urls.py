from django.urls import path

from . import views

app_name = "Apps.ventas"
urlpatterns = [
    path('', views.ListaVentasView, name='lista_ventas'),
    path('agregar', views.VistaAgregarVentas, name='agregar_ventas'),
    path('Abonar/<str:id_venta>/', 
        views.abonar_transaccion, name='agregar_abono'),


    #-----reportes---    
     path('report', views.VentasView, name='report'),
     path('generar_reporte_excel/<str:start_date>/<str:end_date>/', views.generar_reporte_excel, name='generar_reporte_excel'),
     path('generar_reporte_cliente_excel/<int:id_cliente>/', views.generar_reporte_cliente_excel, name='generar_reporte_cliente_excel'),
   
    path('generar_reporte_abonos_cliente/<str:start_date>/<str:end_date>/', views.generar_reporte_abonos_clientes_excel, name='generar_reporte_abonos_cliente'),




]
