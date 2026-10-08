#!/usr/bin/env python
"""
Pruebas de Chapikids.

ANTES este script usaba `Client()` sin base de datos de prueba, así que
`probar_modelo_slug()` creaba y borraba filas en el `db.sqlite3` de
verdad: cada corrida dejaba basura, y si fallaba a media ruta la dejaba
permanente. Ahora usa `TestCase`, que corre contra una base de datos
temporal y la destruye al terminar.

Uso:
    python manage.py test
    (o bien: pytest, si instalas pytest-django)
"""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapikids.settings')
django.setup()

from django.test import Client, TestCase  # noqa: E402
from django.urls import reverse  # noqa: E402

from catalogo.models import Categoria, Producto  # noqa: E402


class PaginasticasTestCase(TestCase):
    """Las páginas públicas responden y muestran lo que deben."""

    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(nombre='Prueba')
        cls.producto = Producto.objects.create(
            nombre='Producto de prueba',
            categoria=cls.categoria,
            precio=100,
            disponible=True,
        )

    def test_paginas_publicas(self):
        for url in [
            reverse('catalogo:lista'),
            reverse('catalogo:nosotros'),
            '/carrito/',
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_checkout_sin_carrito_redirige(self):
        """Sin productos en el carrito, el checkout manda al carrito.

        No es un error: es el flujo correcto. Antes no se probaba.
        """
        respuesta = self.client.get('/pedidos/checkout/')
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/carrito/', respuesta.url)
    def test_detalle_de_producto(self):
        url = f"/producto/{self.producto.slug}/"
        self.assertEqual(self.client.get(url).status_code, 200)


class SlugTestCase(TestCase):
    """El slug se genera solo y no se repite."""

    def test_slug_automatico(self):
        categoria = Categoria.objects.create(nombre='Otra')
        producto = Producto.objects.create(
            nombre='Piñata Test Automatico',
            categoria=categoria,
            precio=100,
        )
        self.assertEqual(producto.slug, 'pinata-test-automatico')
        # El registro se crea dentro de la base de prueba y desaparece
        # al terminar, así que no hay que borrar nada a mano.


class CarritoTestCase(TestCase):
    """El carrito y, sobre todo, el caso que antes lo rompía."""

    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(nombre='Prenda')
        cls.vestido = Producto.objects.create(
            nombre='Vestido', categoria=cls.categoria, precio=100,
            disponible=True,
        )
        cls.blusa = Producto.objects.create(
            nombre='Blusa', categoria=cls.categoria, precio=80,
            disponible=True,
        )

    def test_agregar_al_carrito(self):
        self.client.post(f'/carrito/agregar/{self.vestido.pk}/')
        self.assertEqual(
            self.client.session['carrito'],
            {str(self.vestido.pk): {'cantidad': 1}},
        )

    def test_no_se_agrega_un_producto_no_disponible(self):
        self.vestido.disponible = False
        self.vestido.save()
        self.client.post(f'/carrito/agregar/{self.vestido.pk}/')
        self.assertEqual(self.client.session.get('carrito', {}), {})

    def test_producto_desactivado_no_rompe_el_carrito(self):
        """Regresión: esto devolvía 404 y caía toda la página.

        Si el negocio desactiva un producto que el cliente ya tenía, el
        carrito debe seguir mostrando los demás, no reventar.
        """
        self.client.post(f'/carrito/agregar/{self.vestido.pk}/', {'cantidad': 2})
        self.client.post(f'/carrito/agregar/{self.blusa.pk}/')

        # El negocio desactiva el vestido.
        self.vestido.disponible = False
        self.vestido.save()

        respuesta = self.client.get('/carrito/')

        self.assertEqual(
            respuesta.status_code, 200,
            'El carrito no debe romperse si un producto se desactiva',
        )
        nombres = [i['producto'].nombre for i in respuesta.context['items']]
        self.assertEqual(nombres, ['Blusa'])

    def test_cantidad_invalida_no_revierte_la_pagina(self):
        """Antes `int('mucho')` levantaba ValueError y daba error 500."""
        self.client.post(f'/carrito/agregar/{self.vestido.pk}/')
        respuesta = self.client.post(
            f'/carrito/actualizar/{self.vestido.pk}/', {'cantidad': 'mucho'}
        )
        self.assertEqual(respuesta.status_code, 302)


class FolioTestCase(TestCase):
    """El folio de los pedidos se numera sin repetirse."""

    def test_folios_consecutivos(self):
        from pedidos.models import Pedido

        primero = Pedido.objects.create(
            cliente_nombre='Ana', fecha_evento='2030-01-01'
        )
        segundo = Pedido.objects.create(
            cliente_nombre='Luis', fecha_evento='2030-01-01'
        )

        n1 = int(primero.folio.split('-')[-1])
        n2 = int(segundo.folio.split('-')[-1])
        self.assertEqual(n2, n1 + 1)
        self.assertTrue(primero.folio.startswith('PED-'))


class AdminTestCase(TestCase):
    def test_el_admin_responde(self):
        self.assertEqual(self.client.get('/admin/login/').status_code, 200)


if __name__ == '__main__':
    import unittest

    unittest.main(verbosity=2)