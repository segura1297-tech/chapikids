from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.ver_carrito, name='ver'),
    path('agregar/<int:producto_id>/', views.agregar, name='agregar'),
    path('quitar/<int:producto_id>/', views.quitar, name='quitar'),
    path('actualizar/<int:producto_id>/', views.actualizar_cantidad, name='actualizar'),
    path('limpiar/', views.limpiar, name='limpiar'),
]
