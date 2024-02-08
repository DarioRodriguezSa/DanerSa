from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Compra
from Apps.inventario.models import Producto
from .forms import CompraForm
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
from django.contrib import messages



@login_required(login_url="/accounts/login/")
def sales_list_view(request):
    compras = Compra.objects.all()
    return render(request, "compras/compras.html", {'compras': compras})

@login_required(login_url="/accounts/login/")
def show_realizar_compra(request):
    compras = Compra.objects.all()
    productos = Producto.objects.all()
    inventario_info = [{'nombre': producto.nombre, 'existencia': producto.existencia} for producto in productos]
    return render(request, 'compras/realizar_compra.html', {'compras': compras, 'inventario_info': inventario_info})

@login_required(login_url="/accounts/login/")
def realizar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            
            # Captura la fecha actual
            compra.fecha = date.today()

            # Lógica para actualizar existencia y costo promedio
            actualizar_existencia(compra)
            actualizar_costo_promedio(compra)

            compra.save()

            # Obtener información actualizada del inventario
            productos = Producto.objects.all()
            inventario_info = [{'nombre': producto.nombre, 'existencia': producto.existencia} for producto in productos]

            messages.success(request, 'Compra realizada exitosamente.',  extra_tags='success important')


            # Redirigir a la página de compras
            return redirect('Apps.compras:compras')

    else:
        form = CompraForm()

    # Obtén la fecha actual en formato "AAAA-MM-DD"
    fecha_actual = date.today().strftime('%Y-%m-%d')

    # Obtener información inicial del inventario
    productos = Producto.objects.all()
    inventario_info = [{'nombre': producto.nombre, 'existencia': producto.existencia} for producto in productos]

    return render(request, 'compras/realizar_compra.html', {'form': form, 'fecha_actual': fecha_actual, 'inventario_info': inventario_info})



def actualizar_existencia(compra):
    # Convertir cantidad a Decimal
    cantidad_decimal = Decimal(str(compra.cantidad))

    # Sumar la cantidad convertida a la existencia del producto
    compra.producto.existencia += cantidad_decimal



def actualizar_costo_promedio(compra):
    try:
        producto = Producto.objects.get(idproducto=compra.producto.idproducto)
    except Producto.DoesNotExist:
        # Manejar el caso en el que el producto no existe
        return

    # Guarda el producto con el nuevo precio_compra
    producto.save()