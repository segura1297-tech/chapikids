from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Producto, Categoria, Nosotros


def lista_productos(request):
    """Vista pública del catálogo con buscador y filtro por categoría."""
    productos = Producto.objects.filter(disponible=True)
    categorias = Categoria.objects.filter(activa=True)

    # Filtro por categoría
    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)

    # Buscador
    query = request.GET.get('q', '').strip()
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )

    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': categoria_slug,
        'query': query,
    }
    return render(request, 'catalogo/lista_productos.html', context)


def detalle_producto(request, slug):
    """Vista de detalle de un producto."""
    producto = get_object_or_404(Producto, slug=slug, disponible=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria,
        disponible=True
    ).exclude(pk=producto.pk)[:4]

    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'catalogo/detalle_producto.html', context)


def nosotros(request):
    """Vista de la página 'Quiénes Somos'."""
    try:
        info = Nosotros.objects.filter(activo=True).latest('actualizado')
    except Nosotros.DoesNotExist:
        info = None

    context = {
        'info': info,
    }
    return render(request, 'catalogo/nosotros.html', context)


# ==================== GESTIÓN (solo admin) ====================

@staff_member_required
def gestion_productos(request):
    """Vista para gestionar productos - redirige al admin."""
    return redirect('/admin/catalogo/producto/')


@staff_member_required
def gestion_categorias(request):
    """Vista para gestionar categorías - redirige al admin."""
    return redirect('/admin/catalogo/categoria/')


@staff_member_required
def editar_nosotros(request):
    """Vista para editar Nosotros - redirige al admin."""
    return redirect('/admin/catalogo/nosotros/')
