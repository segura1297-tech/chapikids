from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # Vistas públicas
    path('', views.lista_productos, name='lista'),
    path('producto/<slug:slug>/', views.detalle_producto, name='detalle'),
    path('nosotros/', views.nosotros, name='nosotros'),

    # Gestión (solo admin - redirige al admin de Django)
    path('gestion/productos/', views.gestion_productos, name='gestion_productos'),
    path('gestion/categorias/', views.gestion_categorias, name='gestion_categorias'),
    path('gestion/nosotros/', views.editar_nosotros, name='editar_nosotros'),
]
