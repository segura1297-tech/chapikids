from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote
from .models import Pedido, PedidoItem


def checkout(request):
    """Procesa el pedido y genera el enlace de WhatsApp."""
    carrito = request.session.get('carrito', {})

    if not carrito:
        return redirect('carrito:ver')

    if request.method == 'POST':
        # Obtener datos del formulario
        cliente_nombre = request.POST.get('cliente_nombre', '').strip()
        cliente_telefono = request.POST.get('cliente_telefono', '').strip()
        cliente_email = request.POST.get('cliente_email', '').strip()
        fecha_evento = request.POST.get('fecha_evento', '').strip()
        notas = request.POST.get('notas', '').strip()

        if not cliente_nombre or not cliente_telefono or not fecha_evento:
            return render(request, 'pedidos/checkout.html', {
                'error': 'Por favor completa todos los campos obligatorios.',
                'carrito': carrito,
            })

        # Calcular total
        from catalogo.models import Producto
        total = 0
        items_data = []
        for producto_id, item in carrito.items():
            producto = Producto.objects.get(pk=producto_id)
            subtotal = producto.precio * item['cantidad']
            total += subtotal
            items_data.append({
                'producto': producto,
                'cantidad': item['cantidad'],
                'precio_unitario': producto.precio,
                'subtotal': subtotal,
            })

        # Crear pedido
        pedido = Pedido.objects.create(
            cliente_nombre=cliente_nombre,
            cliente_telefono=cliente_telefono,
            cliente_email=cliente_email,
            fecha_evento=fecha_evento,
            notas=notas,
            total=total,
        )

        # Crear items del pedido
        for item in items_data:
            PedidoItem.objects.create(
                pedido=pedido,
                producto=item['producto'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario'],
            )

        # Generar mensaje de WhatsApp
        mensaje = f"""¡Hola! Quiero hacer un pedido en Chapikids Piñatas 🎉

*Pedido:* {pedido.folio}
*Fecha del evento:* {fecha_evento}

*Productos:*
"""
        for item in items_data:
            mensaje += f"• {item['cantidad']}x {item['producto'].nombre} - ${item['subtotal']:.2f}\n"

        mensaje += f"""
*Total:* ${total:.2f}

*Datos del cliente:*
Nombre: {cliente_nombre}
Teléfono: {cliente_telefono}
"""
        if cliente_email:
            mensaje += f"Email: {cliente_email}\n"
        if notas:
            mensaje += f"\n*Notas:* {notas}\n"

        mensaje += "\n¡Gracias por su preferencia! 🦄"

        # Generar enlace de WhatsApp
        whatsapp_number = settings.WHATSAPP_NUMBER
        mensaje_codificado = quote(mensaje)
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={mensaje_codificado}"

        # Limpiar carrito
        request.session['carrito'] = {}
        request.session.modified = True

        return render(request, 'pedidos/pedido_exitoso.html', {
            'pedido': pedido,
            'whatsapp_url': whatsapp_url,
        })

    return render(request, 'pedidos/checkout.html', {
        'carrito': carrito,
    })
