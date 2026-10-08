from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from catalogo.models import Producto


def _productos_del_carrito(carrito):
    """Trae los productos que siguen disponibles.

    Antes se usaba get_object_or_404 dentro del bucle, y eso rompía la
    página entera: si el negocio desactivaba un producto que alguien ya
    tenía en el carrito, salía 404 y el cliente perdía también los
    productos que sí estaban disponibles. Ahora se filtran y se avisa.
    """
    ids = list(carrito.keys())
    return {
        str(p.pk): p
        for p in Producto.objects.filter(pk__in=ids, disponible=True)
    }


def _limpiar_ids_invalidos(request):
    """Quita del carrito los ids que ya no corresponden a productos."""
    carrito = request.session.get('carrito', {})
    disponibles = {
        str(pk)
        for pk in Producto.objects.filter(
            pk__in=list(carrito.keys()), disponible=True
        ).values_list('pk', flat=True)
    }
    limpio = {k: v for k, v in carrito.items() if k in disponibles}
    if limpio != carrito:
        request.session['carrito'] = limpio
        request.session.modified = True
    return limpio


def ver_carrito(request):
    """Muestra el carrito de compras."""
    _limpiar_ids_invalidos(request)
    carrito = request.session.get('carrito', {})

    # Una sola consulta para todos los productos, en vez de una por
    # producto. Antes el bucle hacía N+1.
    productos = _productos_del_carrito(carrito)

    items = []
    total = 0

    for producto_id, item in carrito.items():
        producto = productos.get(str(producto_id))
        if producto is None:
            # El producto ya no está disponible: se omite en vez de
            # romper la página entera.
            continue

        cantidad = int(item.get('cantidad', 1))
        subtotal = producto.precio * cantidad
        total += subtotal

        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    context = {
        'items': items,
        'total': total,
        'cantidad_items': sum(i['cantidad'] for i in items),
    }
    return render(request, 'carrito/carrito.html', context)


@require_POST
def agregar(request, producto_id):
    """Agrega un producto al carrito."""
    producto = get_object_or_404(Producto, pk=producto_id, disponible=True)

    try:
        cantidad = max(1, int(request.POST.get('cantidad', 1)))
    except (TypeError, ValueError):
        cantidad = 1

    carrito = request.session.get('carrito', {})
    clave = str(producto_id)

    carrito[clave] = {'cantidad': carrito.get(clave, {}).get('cantidad', 0) + cantidad}
    request.session['carrito'] = carrito
    request.session.modified = True

    messages.success(request, f"{producto.nombre} agregado al carrito.")
    return redirect('carrito:ver')


@require_POST
def quitar(request, producto_id):
    """Quita un producto del carrito."""
    carrito = request.session.get('carrito', {})
    clave = str(producto_id)

    if clave in carrito:
        del carrito[clave]
        request.session['carrito'] = carrito
        request.session.modified = True

        producto = Producto.objects.filter(pk=producto_id).first()
        nombre = producto.nombre if producto else 'El producto'
        messages.success(request, f"{nombre} se quitó del carrito.")

    return redirect('carrito:ver')


@require_POST
def actualizar_cantidad(request, producto_id):
    """Actualiza la cantidad de un producto desde la página del carrito."""
    carrito = request.session.get('carrito', {})
    clave = str(producto_id)

    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (TypeError, ValueError):
        # Cantidad ilegible ("mucho", "3.5"): antes esto reventaba la
        # página con un ValueError. Ahora avisa y deja el carrito igual.
        messages.warning(
            request,
            "La cantidad no es válida. Se dejó el carrito igual."
        )
        return redirect('carrito:ver')

    if clave in carrito:
        if cantidad > 0:
            carrito[clave]['cantidad'] = cantidad
        else:
            del carrito[clave]

        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, "Cantidad actualizada.")

    return redirect('carrito:ver')


@require_POST
def limpiar(request):
    """Vacía el carrito completamente."""
    if request.session.get('carrito'):
        request.session['carrito'] = {}
        request.session.modified = True
        messages.success(request, "Carrito vacío.")
    return redirect('carrito:ver')