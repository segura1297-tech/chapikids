#!/usr/bin/env python
"""
Script de pruebas automatizadas para Chapikids Piñatas.
Ejecutar después de cada modificación para verificar que todo funciona.

Uso: python pruebas.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapikids.settings')
django.setup()

from django.test import Client


def probar_paginas():
    """Prueba las páginas públicas."""
    print("=" * 50)
    print("PRUEBAS DE PAGINAS PUBLICAS")
    print("=" * 50)

    c = Client()

    paginas = [
        ('/', 'Catalogo publico'),
        ('/nosotros/', 'Pagina Quienes Somos'),
        ('/carrito/', 'Carrito de compras'),
        ('/pedidos/checkout/', 'Checkout'),
    ]

    for url, nombre in paginas:
        try:
            response = c.get(url)
            estado = "OK" if response.status_code == 200 else "ERROR"
            print(f"{estado} {nombre}: {response.status_code}")
        except Exception as e:
            print(f"ERROR {nombre}: {e}")


def probar_detalle_producto():
    """Prueba la página de detalle de un producto."""
    print("\n" + "=" * 50)
    print("PRUEBA DE DETALLE DE PRODUCTO")
    print("=" * 50)

    c = Client()

    try:
        response = c.get('/producto/pinata-luigi/')
        estado = "OK" if response.status_code == 200 else "ERROR"
        print(f"{estado} Detalle producto: {response.status_code}")

        # Verificar elementos clave
        contenido = response.content.decode('utf-8')
        checks = [
            ('tabs-container', 'Pestanas'),
            ('specs-table', 'Tabla de caracteristicas'),
            ('thumbnail-gallery', 'Galeria de miniaturas'),
            ('add-to-cart-large', 'Boton agregar al carrito'),
        ]

        for patron, nombre in checks:
            presente = "OK" if patron in contenido else "FALTA"
            print(f"{presente} {nombre}")

    except Exception as e:
        print(f"ERROR: {e}")


def probar_modelo_slug():
    """Prueba que el slug se genere automáticamente."""
    print("\n" + "=" * 50)
    print("PRUEBA DE SLUG AUTOMATICO")
    print("=" * 50)

    from catalogo.models import Producto, Categoria

    try:
        cat = Categoria.objects.first()
        producto = Producto.objects.create(
            nombre='Test Slug Automatico',
            categoria=cat,
            precio=100,
        )
        print(f"OK Slug generado: {producto.slug}")
        producto.delete()
        print("OK Producto de prueba eliminado")
    except Exception as e:
        print(f"ERROR: {e}")


def probar_admin():
    """Prueba acceso al admin."""
    print("\n" + "=" * 50)
    print("PRUEBA DE ADMIN")
    print("=" * 50)

    c = Client()

    try:
        response = c.get('/admin/login/')
        estado = "OK" if response.status_code == 200 else "ERROR"
        print(f"{estado} Admin login: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == '__main__':
    print("\n== INICIANDO PRUEBAS DE CHAPMKIDS PIÑATAS ==\n")
    probar_paginas()
    probar_detalle_producto()
    probar_modelo_slug()
    probar_admin()
    print("\n" + "=" * 50)
    print("PRUEBAS COMPLETADAS")
    print("=" * 50 + "\n")
