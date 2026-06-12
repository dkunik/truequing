from django.contrib import admin

from .models import AlbumUsuario, Coleccion, Figurita, Pais, MovimientoAlbum


admin.site.register(Coleccion)
admin.site.register(Pais)
admin.site.register(Figurita)
admin.site.register(AlbumUsuario)
admin.site.register(MovimientoAlbum)
