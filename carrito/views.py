from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalogo.models import Producto


def ver_carrito(request):
    """Muestra el carrito de compras."""
    carrito = request.session.get('carrito', {})
    items = []
    total = 0

    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, pk=producto_id, disponible=True)
        subtotal = producto.precio * item['cantidad']
        items.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'subtotal': subtotal,
        })
        total += subtotal

    context = {
        'items': items,
        'total': total,
        'cantidad_items': sum(item['cantidad'] for item in items),
    }
    return render(request, 'carrito/carrito.html', context)


@require_POST
def agregar(request, producto_id):
    """Agrega un producto al carrito."""
    producto = get_object_or_404(Producto, pk=producto_id, disponible=True)
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {'cantidad': 1}

    request.session['carrito'] = carrito
    request.session.modified = True

    return redirect('carrito:ver')


@require_POST
def quitar(request, producto_id):
    """Quita un producto del carrito."""
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('carrito:ver')


@require_POST
def actualizar_cantidad(request, producto_id):
    """Actualiza la cantidad de un producto en el carrito."""
    carrito = request.session.get('carrito', {})
    cantidad = int(request.POST.get('cantidad', 1))

    if str(producto_id) in carrito:
        if cantidad > 0:
            carrito[str(producto_id)]['cantidad'] = cantidad
        else:
            del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('carrito:ver')


@require_POST
def limpiar(request):
    """Vacía el carrito completamente."""
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect('carrito:ver')
