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
            from catalogo.models import Producto
            items = []
            for producto_id, item in carrito.items():
                producto = Producto.objects.get(pk=producto_id)
                items.append({'producto': producto, 'cantidad': item['cantidad']})
            return render(request, 'pedidos/checkout.html', {
                'error': 'Por favor completa todos los campos obligatorios.',
                'items': items,
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
        from datetime import datetime
        fecha_evento_fmt = fecha_evento
        try:
            fecha_evento_fmt = datetime.strptime(fecha_evento, '%Y-%m-%d').strftime('%d-%m-%Y')
        except ValueError:
            pass

        mensaje = "Hola 👋, buenas tardes:\n\n"
        for item in items_data:
            mensaje += f"🎉 Quisiera la cotización de la piñata modelo: *{item['producto'].nombre}* (cantidad: {item['cantidad']})\n"
            mensaje += f"📅 El evento lo tengo programado para: {fecha_evento_fmt}\n"
            if item['producto'].tiempo_entrega:
                mensaje += f"⏱️ Tiempo de entrega estimado: {item['producto'].tiempo_entrega}\n"
            mensaje += "\n"

        mensaje += f"👤 Cliente: {cliente_nombre}\n"
        mensaje += f"📱 Teléfono: {cliente_telefono}\n"
        if cliente_email:
            mensaje += f"📧 Email: {cliente_email}\n"
        if notas:
            mensaje += f"📝 Notas: {notas}\n"
        mensaje += f"\nGracias 🙏"

        # Incluir URLs de las imágenes del producto
        for item in items_data:
            if item['producto'].foto:
                url_imagen = request.build_absolute_uri(item['producto'].foto.url)
                mensaje += f"\n\n📷 Imagen {item['producto'].nombre}: {url_imagen}"

        mensaje += "\n\n¡Gracias por su preferencia! 🦄"

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

    # Construir items para mostrar
    from catalogo.models import Producto
    items = []
    for producto_id, item in carrito.items():
        producto = Producto.objects.get(pk=producto_id)
        items.append({'producto': producto, 'cantidad': item['cantidad']})

    return render(request, 'pedidos/checkout.html', {
        'items': items,
    })
