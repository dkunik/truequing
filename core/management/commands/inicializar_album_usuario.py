from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from core.models import Coleccion
from core.services import inicializar_album_usuario


class Command(BaseCommand):
    help = "Inicializa el álbum vacío de un usuario para una colección"

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("coleccion")

    def handle(self, *args, **options):
        username = options["username"]
        nombre_coleccion = options["coleccion"]

        User = get_user_model()

        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"No existe el usuario {username}")

        try:
            coleccion = Coleccion.objects.get(nombre=nombre_coleccion)
        except Coleccion.DoesNotExist:
            raise CommandError(f"No existe la colección {nombre_coleccion}")

        inicializar_album_usuario(usuario, coleccion)

        self.stdout.write(
            self.style.SUCCESS(
                f"Álbum inicializado para {username} / {nombre_coleccion}"
            )
        )
