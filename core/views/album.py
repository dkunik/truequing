from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from core.models import AlbumUsuario
from core.services import agregar_figurita, quitar_figurita


@login_required
def mi_album(request):
    album = (
        AlbumUsuario.objects
        .filter(usuario=request.user)
        .select_related(
            "figurita",
            "figurita__pais",
        )
        .order_by(
            "figurita__pais__nombre",
            "figurita__numero",
        )
    )

    paises = {}

    for item in album:
        pais = item.figurita.pais

        if pais not in paises:
            paises[pais] = []

        paises[pais].append(item)

    return render(request, "core/mi_album.html", {
        "paises": paises,
    })


@login_required
@require_POST
def actualizar_figurita_album(request):
    item_id = request.POST.get("item_id")
    accion = request.POST.get("accion")

    item = get_object_or_404(
        AlbumUsuario,
        id=item_id,
        usuario=request.user,
    )

    if accion == "sumar":
        item = agregar_figurita(
            usuario=request.user,
            figurita=item.figurita,
            tipo="manual",
            descripcion="Carga desde Mi Álbum",
        )

    elif accion == "restar":

        if item.cantidad <= 0:
            return JsonResponse(
                {
                    "ok": False,
                    "error": "La cantidad no puede ser negativa.",
                    "cantidad": item.cantidad,
                },
                status=400,
            )

        item = quitar_figurita(
            usuario=request.user,
            figurita=item.figurita,
            tipo="manual",
            descripcion="Carga desde Mi Álbum",
        )

    else:
        return JsonResponse(
            {
                "ok": False,
                "error": "Acción inválida.",
            },
            status=400,
        )

    return JsonResponse({
        "ok": True,
        "item_id": item.id,
        "cantidad": item.cantidad,
    })
