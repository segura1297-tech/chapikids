from django.contrib import admin
from .models import Categoria, Producto, ProductoImagen, Nosotros


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ['imagen', 'descripcion', 'orden']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'activa', 'orden']
    list_editable = ['activa', 'orden']
    readonly_fields = ['slug']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'disponible', 'destacado', 'personalizable', 'creado']
    list_filter = ['categoria', 'disponible', 'destacado', 'personalizable']
    list_editable = ['precio', 'disponible', 'destacado']
    readonly_fields = ['slug']
    search_fields = ['nombre', 'descripcion']
    inlines = [ProductoImagenInline]

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'slug', 'categoria', 'precio', 'descripcion', 'foto')
        }),
        ('Estado', {
            'fields': ('disponible', 'destacado')
        }),
        ('Características Técnicas', {
            'fields': (('alto', 'ancho', 'profundidad'), 'peso', 'materiales', 'tiempo_elaboracion'),
            'classes': ('collapse',)
        }),
        ('Colores y Personalización', {
            'fields': ('colores_disponibles', 'personalizable', 'opciones_personalizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Nosotros)
class NosotrosAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'activo', 'actualizado']
    list_editable = ['activo']
    readonly_fields = ['actualizado']
