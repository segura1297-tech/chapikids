from django.contrib import admin
from .models import Pedido, PedidoItem


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['folio', 'cliente_nombre', 'fecha_evento', 'estado', 'total', 'creado']
    list_filter = ['estado', 'creado', 'fecha_evento']
    list_editable = ['estado']
    search_fields = ['folio', 'cliente_nombre', 'cliente_telefono']
    readonly_fields = ['folio', 'creado', 'actualizado']
    inlines = [PedidoItemInline]
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('folio', 'estado', 'creado', 'actualizado')
        }),
        ('Datos del Cliente', {
            'fields': ('cliente_nombre', 'cliente_telefono', 'cliente_email')
        }),
        ('Detalles del Evento', {
            'fields': ('fecha_evento', 'notas')
        }),
        ('Total', {
            'fields': ('total',)
        }),
    )
