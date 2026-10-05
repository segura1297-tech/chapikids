# Chapikids Piñatas 🦄🎉

Sistema de catálogo y pedidos para piñatas con cierre de venta por WhatsApp.

## Características

- **Catálogo público**: Productos con foto, precio y categoría
- **Buscador y filtros**: Por nombre y categoría
- **Carrito de compras**: Con sesión de usuario
- **Cierre de venta por WhatsApp**: Enlace automático con mensaje armado
- **Panel de administración**: Gestión de productos y pedidos
- **Diseño responsive**: Optimizado para celular y escritorio

## Requisitos

- Python 3.10+
- pip

## Instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar migraciones**:
   ```bash
   python manage.py migrate
   ```

6. **Cargar datos iniciales** (productos de ejemplo):
   ```bash
   python cargar_datos.py
   ```

7. **Crear superusuario** (para acceder al admin):
   ```bash
   python manage.py createsuperuser
   ```

8. **Levantar el servidor**:
   ```bash
   python manage.py runserver
   ```

9. **Acceder al sitio**:
   - Sitio público: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Estructura del Proyecto

```
chapikids/
├── manage.py              # Comandos de Django
├── requirements.txt       # Dependencias
├── cargar_datos.py        # Script de datos iniciales
├── db.sqlite3            # Base de datos SQLite
├── media/                # Imágenes de productos
├── static/               # Archivos estáticos (CSS, JS)
│   ├── css/
│   └── js/
├── chapikids/            # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── catalogo/             # App de productos
│   ├── models.py         # Categoria, Producto
│   ├── views.py          # Vistas del catálogo
│   └── templates/
├── carrito/              # App de carrito
│   ├── views.py          # Lógica del carrito
│   └── templates/
└── pedidos/              # App de pedidos
    ├── models.py         # Pedido, PedidoItem
    ├── views.py          # Checkout y WhatsApp
    └── templates/
```

## Uso

### Para el Negocio (Administrador)

1. Accede a http://127.0.0.1:8000/admin/
2. Inicia sesión con tu superusuario
3. **Gestionar productos**: Agrega, edita o desactiva piñatas
4. **Gestionar pedidos**: Cambia estados (Nuevo → Confirmado → En preparación → Entregado/Cerrado)

### Para el Cliente

1. Explora el catálogo en http://127.0.0.1:8000/
2. Usa el buscador o filtra por categoría
3. Agrega productos al carrito
4. Finaliza el pedido ingresando tus datos
5. Envía el pedido por WhatsApp con un clic

## Configuración de WhatsApp

El número de WhatsApp del negocio está configurado en `chapikids/settings.py`:

```python
WHATSAPP_NUMBER = '5218282895407'
```

Formato internacional México: `521` + número.

## Estados de Pedido

- **Nuevo**: Pedido recién creado
- **Confirmado**: Pedido confirmado por el negocio
- **En preparación**: Piñata en proceso de elaboración
- **Entregado/Cerrado**: Pedido entregado al cliente
- **Cancelado**: Pedido cancelado

## Personalización

### Colores y Diseño
Edita `static/css/style.css` para cambiar colores y estilos.

### Logo
Reemplaza `media/logo.jpeg` con tu logo.

### Productos
Usa el admin de Django o edita `cargar_datos.py` para modificar los productos iniciales.

## Notas

- El carrito usa sesiones de Django (no requiere login)
- Las imágenes se guardan en `media/productos/`
- La base de datos es SQLite (ideal para desarrollo local)
- Para producción, considera usar PostgreSQL y un servidor como Gunicorn

## Soporte

Para dudas o problemas, contacta al desarrollador o revisa la documentación de Django.

---

¡Gracias por usar Chapikids Piñatas! 🎉🦄
