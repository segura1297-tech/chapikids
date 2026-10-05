#!/usr/bin/env python
"""Script para cargar datos iniciales de Chapikids Piñatas."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapikids.settings')
django.setup()

from catalogo.models import Categoria, Producto


def cargar_datos():
    """Carga categorías y productos de ejemplo."""
    print("Cargando datos iniciales...")

    # Crear categorías
    categorias_data = [
        {'nombre': 'Superhéroes', 'slug': 'superheroes', 'descripcion': 'Piñatas de superhéroes'},
        {'nombre': 'Videojuegos', 'slug': 'videojuegos', 'descripcion': 'Piñatas de videojuegos'},
        {'nombre': 'Princesas', 'slug': 'princesas', 'descripcion': 'Piñatas de princesas'},
        {'nombre': 'Animales/Unicornios', 'slug': 'animales-unicornios', 'descripcion': 'Piñatas de animales y unicornios'},
        {'nombre': 'Cartoon', 'slug': 'cartoon', 'descripcion': 'Piñatas de dibujos animados'},
    ]

    categorias = {}
    for cat_data in categorias_data:
        cat, created = Categoria.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        categorias[cat_data['slug']] = cat
        if created:
            print(f"  Categoría creada: {cat.nombre}")

    # Crear productos
    productos_data = [
        {
            'categoria': 'videojuegos',
            'nombre': 'Piñata Luigi',
            'slug': 'pinata-luigi',
            'descripcion': 'Piñata de Luigi de Super Mario Bros. ¡Perfecta para fiestas de videojuegos!',
            'precio': 350.00,
            'foto': 'media/pinata_luigi.jpeg',
        },
        {
            'categoria': 'videojuegos',
            'nombre': 'Piñata Mario',
            'slug': 'pinata-mario',
            'descripcion': 'Piñata de Mario de Super Mario Bros. ¡El héroe de tu fiesta!',
            'precio': 350.00,
            'foto': 'media/pinata_mario.jpeg',
        },
        {
            'categoria': 'animales-unicornios',
            'nombre': 'Piñata Unicornio 1',
            'slug': 'pinata-unicornio-1',
            'descripcion': 'Hermosa piñata de unicornio con colores pastel. ¡Mágica!',
            'precio': 400.00,
            'foto': 'media/pinata_unicornio1.jpeg',
        },
        {
            'categoria': 'animales-unicornios',
            'nombre': 'Piñata Unicornio 2',
            'slug': 'pinata-unicornio-2',
            'descripcion': 'Piñata de unicornio rosa y blanco. ¡Encantadora!',
            'precio': 400.00,
            'foto': 'media/pinata_unicornio2.jpeg',
        },
    ]

    for prod_data in productos_data:
        prod, created = Producto.objects.get_or_create(
            slug=prod_data['slug'],
            defaults={
                'categoria': categorias[prod_data['categoria']],
                'nombre': prod_data['nombre'],
                'descripcion': prod_data['descripcion'],
                'precio': prod_data['precio'],
                'foto': prod_data['foto'],
            }
        )
        if created:
            print(f"  Producto creado: {prod.nombre}")

    print("¡Datos cargados exitosamente!")


if __name__ == '__main__':
    cargar_datos()
