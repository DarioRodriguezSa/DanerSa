from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente
from Apps.ventas.models import Venta, Transaccion
from Apps.rutas.models import Ruta
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from django.db.models import Q

@login_required(login_url="/accounts/login/")
def ListaClientesView(request):
    context = {
        "clientes": Cliente.objects.filter(activo=True).exclude(id=1),
        "rutas": Ruta.objects.filter(activo=True),
    }
    return render(request, "clientes/clientes.html", context=context)



        
@login_required(login_url="/accounts/login/")
def DetalleClientesView(request, id_cliente):
    cliente = Cliente.objects.get(pk=id_cliente)

    ventas_no_pagadas = Venta.objects.filter(id_clientes=id_cliente, estado_cuenta=True)
    transaccion = Transaccion.objects.all()
    ()

    for venta in ventas_no_pagadas:
        venta.saldo = venta.getSaldo()

    context = {
        "cliente": cliente,
        "ventas": ventas_no_pagadas,
    }
    return render(request, "clientes/detalles_cliente.html", context=context)


@login_required(login_url="/accounts/login/")
def VistaAgregarCliente(request):
    context={
        "rutas": Ruta.objects.filter(activo=True),
    }
    if request.method == 'POST':
        data = request.POST
        attributes = {
            "nombre": data['nombre'],
            "direccion": data['direccion'],
            "telefono": data['telefono'],
        }
        ruta_id = data['ruta_select']
        ruta_instance = Ruta.objects.get(id=ruta_id)
        attributes["ruta"] = ruta_instance
        if Cliente.objects.filter(**attributes).exists():
            messages.error(request, '¡El cliente ya existe!',
                extra_tags="warning")
            return redirect('Apps.clientes:agregar_cliente')
        try:
            new_customer = Cliente.objects.create(**attributes)
            new_customer.save()
            messages.success(request, '¡Cliente: ' + attributes["nombre"] + " " + ' Creado con éxito!', extra_tags="success")
            return redirect('Apps.clientes:lista_clientes')
        except Exception as e:
            messages.success(request, f'Error en cliente: {str(e)}', extra_tags="danger")
            
            return redirect('Apps.clientes:agregar_cliente')
    return render(request, "clientes/agregar_clientes.html",context=context)


@login_required(login_url="/accounts/login/")
def VistaActulizarCliente(request, id_cliente):
    try:
        cliente = Cliente.objects.get(id=id_cliente)
    except Exception as e:
        messages.success(
            request, '¡Hubo un error al intentar localizar al cliente!', extra_tags="danger")
        return redirect('Apps.clientes:lista_clientes')
    context = {
        "cliente": cliente,
    }
    if request.method == 'POST':
        try:
            data = request.POST
            attributes = {
                "nombre": data['nombre'],
                "direccion": data['direccion'],
                "telefono": data['telefono'],
            }
            ruta_id = data['ruta_select']
            ruta_instance = Ruta.objects.get(id=ruta_id)
            attributes["ruta"] = ruta_instance
            cliente = Cliente.objects.filter(
                id=id_cliente).update(**attributes)
            cliente = Cliente.objects.get(id=id_cliente)
            messages.success(request, '¡Cliente: ' + cliente.nombre +
                ' actualizado exitosamente!', extra_tags="success")
            return redirect('Apps.clientes:lista_clientes')
        except Exception as e:
            messages.success(
                request, '¡Hubo un error durante la actualización!', extra_tags="danger")
            return redirect('Apps.clientes:lista_clientes')
    return render(request, "clientes/actualizar_ clientes.html", context=context)


@login_required(login_url="/accounts/login/")
def VistaEliminarCliente(request, id_cliente):
    try:
        cliente = Cliente.objects.get(id=id_cliente)
        cliente.activo = False
        cliente.save()
        messages.success(request, '¡Cliente: ' + cliente.nombre +
            ' Eliminado!', extra_tags="success")
        return redirect('Apps.clientes:lista_clientes')
    except Exception as e:
        messages.success(
            request, '¡Hubo un error durante la eliminación!', extra_tags="danger")
        return redirect('Apps.clientes:lista_clientes')
    
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def GetClientsAJAXView(request):
    if request.method == 'POST':
        if is_ajax(request=request):
            data = []
            clientes = Cliente.objects.filter(nombre__icontains=request.POST['term'],activo=True)
            for cliente in clientes[0:10]:
                item = cliente.to_json()
                data.append(item)

            return JsonResponse(data, safe=False)
        


#para reportes---------------
def VistaCliente(request):
    clientes = Cliente.objects.filter(activo=True)
    print(clientes)  # Añadir esta línea para imprimir los clientes en la consola
    context = {
        "clientes": clientes,
    }

    return render(request, "ventas/Vreport.html", context=context)
