from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path
from Apps.pos.views import ListaVentasgraph  # Importa la vista desde el espacio de nombres "Apps.pos"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Apps.pos.urls')),
    path('', include('Apps.authentication.urls')),
    path('inventario/', include('Apps.inventario.urls')),
    path('clientes/', include('Apps.clientes.urls')),
    path('ventas/', include('Apps.ventas.urls')),
    path('compras/', include('Apps.compras.urls')),
    path('rutas/', include('Apps.rutas.urls')),
    
]
