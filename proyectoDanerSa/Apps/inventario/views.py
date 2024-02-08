from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from decimal import Decimal, InvalidOperation
from django.http import HttpResponseBadRequest


@login_required(login_url="/accounts/login/")
def index(request):
    productos = Producto.objects.all()
    return render(request, "inventario/index.html", {'productos': productos})




@login_required(login_url="/accounts/login/")
@csrf_protect
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, idproducto=producto_id)

    if request.method == 'POST' and producto.estado != Producto.INACTIVO:
        # Cambia el estado del producto a inactivo
        producto.estado = Producto.INACTIVO
        producto.save()
        messages.success(request, '')
        return JsonResponse({'success': True, 'message': 'El producto fue marcado como inactivo.'})

    return JsonResponse({'success': False, 'message': 'No se pudo eliminar el producto.'})



@login_required(login_url="/accounts/login/")
def modificar_producto(request, producto_id):
    producto = get_object_or_404(Producto, idproducto=producto_id)

    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre', producto.nombre)

        existencia = request.POST.get('existencia', '')
        try:
            existencia = float(existencia)
            if existencia < 0:
                raise ValueError("La existencia no puede ser un número negativo.")
            producto.existencia = existencia
        except ValueError:
            return HttpResponseBadRequest("Error: La existencia debe ser un número válido y no puede ser negativa.")

        precio_venta = request.POST.get('precio_venta', '')
        try:
            precio_venta = Decimal(precio_venta)
            if precio_venta < 0:
                raise ValueError("El precio de venta no puede ser un número negativo.")
            producto.precio_venta = precio_venta
        except InvalidOperation:
            return HttpResponseBadRequest("Error: El precio de venta debe ser un número válido y no puede ser negativo.")

        precio_compra = request.POST.get('precio_compra', '')
        try:
            precio_compra = Decimal(precio_compra)
            if precio_compra < 0:
                raise ValueError("El precio de compra no puede ser un número negativo.")
            if precio_compra > producto.precio_venta:
                raise ValueError("El precio de compra no puede ser mayor que el precio de venta.")
            producto.precio_compra = precio_compra
        except InvalidOperation:
            return HttpResponseBadRequest("Error: El precio de compra debe ser un número válido y no puede ser negativo.")

        producto.estado = int(request.POST.get('estado', producto.estado))

        producto.save()

        # Aquí defines los mensajes de éxito o error según sea necesario
        mensaje = 'Producto modificado exitosamente'
        # Si hay algún error en la validación, puedes definir los mensajes de error aquí
        mensaje_nombre = "Mensaje de error para el nombre"
        mensaje_existencia = "Mensaje de error para la existencia"
        mensaje_precio_venta = "Mensaje de error para el precio de venta"
        mensaje_precio_compra = "Mensaje de error para el precio de compra"

        return render(request, "inventario/index.html", {'producto': producto,
                                                        'mensaje_nombre': mensaje_nombre,
                                                        'mensaje_existencia': mensaje_existencia,
                                                        'mensaje_precio_venta': mensaje_precio_venta,
                                                        'mensaje_precio_compra': mensaje_precio_compra})


    return render(request, "inventario/index.html", {'producto': producto})





@login_required(login_url="/accounts/login/")
def VistaAgregarProducto(request):
    if request.method == 'POST':
        data = request.POST
        nombre = data['nombre']
        existencia = float(data['existencia'])
        precio_venta = Decimal(data['precio_venta'])
        precio_compra = Decimal(data['precio_compra'])
        estado = int(data['estado'])
        
        if precio_compra >= precio_venta:
            messages.error(request, '¡El precio de compra debe ser menor que el precio de venta!', extra_tags="warning")
            return redirect('Apps.inventario:agregar_producto')
        
        if Producto.objects.filter(nombre=nombre).exists():
            messages.error(request, '¡El producto ya existe!', extra_tags="warning")
            return redirect('Apps.inventario:agregar_producto')
        
        try:
            new_product = Producto.objects.create(
                nombre=nombre,
                existencia=existencia,
                precio_venta=precio_venta,
                precio_compra=precio_compra,
                estado=estado
            )
            messages.success(request, '¡Producto: ' + nombre + ' creado con éxito!', extra_tags="success")
            return redirect('Apps.inventario:index')
        except Exception as e:
            messages.error(request, '¡Hubo un error durante la creación!', extra_tags="danger")
            print(e)
            return redirect('Apps.inventario:agregar_producto')
    
    return render(request, "inventario/agregar_producto.html")