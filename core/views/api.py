from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.models import AlbumUsuario


@login_required
def api_mi_album(request):
    items = (
        AlbumUsuario.objects
        .filter(usuario=request.user)
        .select_related(
            "figurita",
            "figurita__pais",
            "figurita__coleccion",
        )
        .order_by(
            "figurita__pais__nombre",
            "figurita__numero",
        )
    )

    data = []

    for item in items:
        data.append({
            "figurita_id": item.figurita.id,
            "pais": item.figurita.pais.nombre,
            "pais_codigo": item.figurita.pais.codigo,
            "numero": item.figurita.numero,
            "cantidad": item.cantidad,
            "coleccion": item.figurita.coleccion.nombre,
        })

    return JsonResponse({
    "usuario": request.user.username,
    "coleccion": data[0]["coleccion"] if data else "Mundial 2026",
    "album": data,
})
