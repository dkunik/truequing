from django.contrib.auth import get_user_model
from core.models import Coleccion
from core.services import exportar_estado_canje_compacto, decodificar_estado_canje_compacto
from core.types import EstadoCanje

User = get_user_model()

emil = User.objects.get(username="emil")
coleccion = Coleccion.objects.get(nombre="Mundial 2026")

payload = exportar_estado_canje_compacto(emil, coleccion)

estado = decodificar_estado_canje_compacto(payload, coleccion)

print(estado)
print(type(estado))
