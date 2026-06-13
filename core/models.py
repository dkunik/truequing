from django.conf import settings
from django.db import models


class Coleccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Pais(models.Model):
    coleccion = models.ForeignKey(
        Coleccion,
        on_delete=models.CASCADE,
        related_name="paises",
    )
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["coleccion", "codigo"],
                name="pais_unico_por_coleccion_codigo",
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.coleccion})"


class Figurita(models.Model):
    coleccion = models.ForeignKey(
        Coleccion,
        on_delete=models.CASCADE,
        related_name="figuritas",
    )
    pais = models.ForeignKey(
        Pais,
        on_delete=models.CASCADE,
        related_name="figuritas",
    )
    numero = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["coleccion", "pais", "numero"],
                name="figurita_unica_por_coleccion_pais_numero",
            )
        ]

    def __str__(self):
        return f"{self.pais.nombre} #{self.numero}"


class AlbumUsuario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="albumes",
    )
    figurita = models.ForeignKey(
        Figurita,
        on_delete=models.CASCADE,
        related_name="usuarios",
    )
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "figurita"],
                name="album_usuario_figurita_unica",
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.figurita} x{self.cantidad}"

class MovimientoAlbum(models.Model):
    TIPO_CHOICES = [
        ("manual", "Carga manual"),
        ("canje", "Canje"),
        ("ajuste", "Ajuste"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="movimientos_album",
    )

    figurita = models.ForeignKey(
        Figurita,
        on_delete=models.CASCADE,
        related_name="movimientos",
    )

    delta = models.IntegerField()

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default="manual",
    )

    descripcion = models.CharField(
        max_length=200,
        blank=True,
    )

    creado = models.DateTimeField(auto_now_add=True)
    sincronizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {self.figurita} ({self.delta:+d})"

class Conversacion(models.Model):

    usuario_a = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="conversaciones_iniciadas",

    )

    usuario_b = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="conversaciones_recibidas",

    )

    fecha_creacion = models.DateTimeField(

        auto_now_add=True,

    )

    class Meta:

        ordering = ["-fecha_creacion"]

    def __str__(self):

        return (

            f"{self.usuario_a.username}"

            f" ↔ "

            f"{self.usuario_b.username}"

        )

class Mensaje(models.Model):

    conversacion = models.ForeignKey(

        Conversacion,

        on_delete=models.CASCADE,

        related_name="mensajes",

    )

    autor = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="mensajes_enviados",

    )

    texto = models.TextField()

    fecha = models.DateTimeField(

        auto_now_add=True,

    )

    class Meta:

        ordering = ["fecha"]

    def __str__(self):

        return (

            f"{self.autor.username}: "

            f"{self.texto[:50]}"

        )
