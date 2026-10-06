from django.db import models
from django.utils.text import slugify
from catalogo.validators import validar_precio_positivo


class Categoria(models.Model):
    """Categoría de productos (personajes o temas)."""
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
            # Evitar duplicados
            original_slug = self.slug
            counter = 1
            while Categoria.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)


class Producto(models.Model):
    """Producto del catálogo de piñatas."""
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_precio_positivo])
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)

    # Características técnicas
    alto = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Alto en cm')
    ancho = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Ancho en cm')
    profundidad = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Profundidad en cm')
    peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='Peso en kg')
    materiales = models.TextField(blank=True, help_text='Materiales de elaboración')
    tiempo_elaboracion = models.CharField(max_length=100, blank=True, help_text='Ej: 3-5 días hábiles')
    tiempo_entrega = models.CharField(max_length=100, blank=True, help_text='Ej: 3-5 días hábiles')
    colores_disponibles = models.CharField(max_length=300, blank=True, help_text='Colores separados por comas')

    # Personalización
    personalizable = models.BooleanField(default=False, help_text='¿Se puede personalizar?')
    opciones_personalizacion = models.TextField(blank=True, help_text='Opciones de personalización')

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-creado']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
            # Evitar duplicados
            original_slug = self.slug
            counter = 1
            while Producto.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def get_dimensiones(self):
        """Retorna las dimensiones formateadas."""
        dims = []
        if self.alto:
            dims.append(f"Alto: {self.alto} cm")
        if self.ancho:
            dims.append(f"Ancho: {self.ancho} cm")
        if self.profundidad:
            dims.append(f"Profundidad: {self.profundidad} cm")
        return " | ".join(dims) if dims else "No especificado"

    def get_colores_lista(self):
        """Retorna lista de colores disponibles."""
        if self.colores_disponibles:
            return [c.strip() for c in self.colores_disponibles.split(',')]
        return []


class ProductoImagen(models.Model):
    """Imágenes adicionales de un producto."""
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='productos/galeria/')
    orden = models.PositiveIntegerField(default=0)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['orden']
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Producto'

    def __str__(self):
        return f"Imagen {self.orden} de {self.producto.nombre}"


class Nosotros(models.Model):
    """Contenido de la sección 'Quiénes Somos'."""
    titulo = models.CharField(max_length=200, default='Quiénes Somos')
    subtitulo = models.CharField(max_length=300, blank=True)
    descripcion = models.TextField()
    mision = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    historia = models.TextField(blank=True)
    foto = models.ImageField(upload_to='nosotros/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nosotros'
        verbose_name_plural = 'Nosotros'

    def __str__(self):
        return self.titulo
