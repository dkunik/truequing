from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.models import Coleccion
from core.services import exportar_estado_canje


@login_required
def mi_estado_canje(request):
    coleccion = Coleccion.objects.get(
        nombre="Mundial 2026"
    )

    estado = exportar_estado_canje(
        request.user,
        coleccion,
    )

    return JsonResponse(
        estado,
        json_dumps_params={
            "indent": 4,
        },
    )
