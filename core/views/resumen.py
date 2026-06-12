from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import AlbumUsuario


def agrupar_por_pais(items):
    paises = {}

    for item in items:
        pais = item.figurita.pais

        if pais not in paises:
            paises[pais] = []

        paises[pais].append(item)

    return paises


@login_required
def mis_repetidas(request):
    items = (
        AlbumUsuario.objects
        .filter(
            usuario=request.user,
            cantidad__gt=1,
        )
        .select_related(
            "figurita",
            "figurita__pais",
        )
        .order_by(
            "figurita__pais__nombre",
            "figurita__numero",
        )
    )

    return render(request, "core/resumen.html", {
        "titulo": "Mis repetidas",
        "descripcion": "Estas son las figuritas que tenés disponibles para canjear.",
        "paises": agrupar_por_pais(items),
    })


@login_required
def mis_faltantes(request):
    items = (
        AlbumUsuario.objects
        .filter(
            usuario=request.user,
            cantidad=0,
        )
        .select_related(
            "figurita",
            "figurita__pais",
        )
        .order_by(
            "figurita__pais__nombre",
            "figurita__numero",
        )
    )

    return render(request, "core/resumen.html", {
        "titulo": "Mis faltantes",
        "descripcion": "Estas son las figuritas que todavía te faltan.",
        "paises": agrupar_por_pais(items),
    })
