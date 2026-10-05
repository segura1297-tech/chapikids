def carrito_context(request):
    """Context processor para mostrar el carrito en todos los templates."""
    carrito = request.session.get('carrito', {})
    cantidad_items = sum(item['cantidad'] for item in carrito.values())
    return {'cantidad_carrito': cantidad_items}
